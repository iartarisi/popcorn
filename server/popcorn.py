from datetime import date

import redis

import tornado.ioloop
import tornado.web

rdb = redis.Redis(host='localhost', port=6379, db=0)

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        total_packages = int(rdb.get('global:nextPackageId'))

        self.write('Packages: %s\n' % total_packages)
        # this is proof that I either don't understand redis yet, or I'm
        # just optimizing too early, or both
        name_keys = ['package:%s:name' % i for i in range(total_packages) if i]
        vote_keys = ['package:%s:voted' % i for i in range(total_packages) if i]
        rec_keys = ['package:%s:recent' % i for i in range(total_packages) if i]
        old_keys = ['package:%s:old' % i for i in range(total_packages) if i]
        nof_keys = ['package:%s:nofiles' % i for i in range(total_packages) if i]

        names = rdb.mget(name_keys)
        voted = rdb.mget(vote_keys)
        recent = rdb.mget(rec_keys)
        old = rdb.mget(old_keys)
        nofiles = rdb.mget(nof_keys)
        
        self.render('index.html',
                    names=names,
                    voted=voted,
                    recent=recent,
                    old=old,
                    nofiles=nofiles)

    def post(self):
        self.set_header("Content-Type", "text/plain")
        try:
            assert self.request.files['popcorn'][0][
                'content_type'] == 'text/plain', tornado.web.HTTPError(415)
        except KeyError:
            raise Exception("nothing uploaded")
        parse_popcorn(self.request.files['popcorn'][0]['body'])

def get_system_id(hw_uuid):
    """Check if the system is in our database and create it if it isn't

    :arg hw-uuid: smolt hw-uuid to uniquely indentify each system

    Returns the internal system_id of this system.

    """
    key = 'hw-uuid:%s' % hw_uuid
    try:
        system_id = rdb[key]
    except KeyError:
        system_id = str(rdb.incr('global:nextSystemId'))
        rdb[key] = system_id
    return system_id

def get_package_id(package_name):
    """Get or create a package_id for this package_name"""
    key = 'packageName:%s' % package_name
    try:
        package_id = rdb[key]
    except KeyError:
        package_id = str(rdb.incr('global:nextPackageId'))
        rdb[key] = package_id
    return package_id

def get_submission(system_id):
    """Get a new submission for this system_id"""
    # create new submission
    sub_id = str(rdb.incr('global:nextSubmissionId'))
    sub_date = date.today().strftime('%y-%m-%d')
    rdb.set('submission:%s:date', sub_date)

    # attach submission to system
    rdb.lpush('system:%s:submissions' % system_id, sub_id)

    return sub_id
    
def parse_popcorn(data):
    datalines = data.splitlines()
    (popcorn, version, arch, hw_uuid) = datalines[0].split()

    system_id = get_system_id(hw_uuid)
    rdb.set('system:%s:arch' % system_id, arch)
    # TODO check if system can submit based on date
    sub = get_submission(system_id)
    rdb.set('submission:%s:popcorn' % sub, version)
    for line in datalines[1:]:
        (status, package_name) = line.split()
        package_id = get_package_id(package_name)
        # create package
        rdb.setnx('package:%s:name' % package_id, package_name)
        if status == 'v':
            rdb.incr('package:%s:voted' % package_id)
        elif status == 'r':
            rdb.incr('package:%s:recent' % package_id)
        elif status == 'o':
            rdb.incr('package:%s:old' % package_id)
        elif status == 'n':
            rdb.incr('package:%s:nofiles' % package_id)
        # add package to the submission
        rdb.lpush('submission:%s:packages' % sub, package_id)
        
application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
