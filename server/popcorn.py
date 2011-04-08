from datetime import date

import redis

import tornado.ioloop
import tornado.web

rdb = redis.Redis(host='localhost', port=6379, db=0)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        hw_uuids = rdb.lrange('hw-uuids', 0, -1)

        total_packages = rdb.get('global:nextPackageId')

        names, voted, recent, old, nofiles = get_sorted_packages()
        self.render('index.html',
                    systems=hw_uuids,
                    total_packages=total_packages,
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

        self.write('Submission received. Thank you!')

class SystemHandler(tornado.web.RequestHandler):
    def get(self, hw_uuid):
        try:
            system_id = rdb['hw-uuid:%s' % hw_uuid]
        except KeyError:
            raise tornado.web.HTTPError(
                404, "Could not find system with hw-uuid %s", hw_uuid)

        arch = rdb.get('system:%s:arch' % system_id)
        self.write("<h2>System: %s - %s</h2>" % (hw_uuid, arch))
        self.write("<p>Submissions: \n</p>")
        subs = rdb.lrange('system:%s:submissions' % system_id, 0, -1)
        for sub in subs:
            self.write("<a href='/submission/%s'>submission %s</a>" % (sub, sub))

class SubmissionHandler(tornado.web.RequestHandler):
    def get(self, sub_id):
        package_ids = rdb.lrange('submission:%s:packages' % sub_id, 0, -1)
        name_keys = ['package:%s:name' % i for i in package_ids]
        package_names = rdb.mget(name_keys)
        self.write('<p>Submission packages:</p>')
        self.write('<ul>')
        for name in package_names:
            self.write('<li>%s</li>' % name)
        self.write('</ul>')
def get_sorted_packages(key='voted'):
    """Get a lists of package attributes sorted by `key`

    The list returned is made of [names, voted, recent, old, nofiles]

    """
    if key not in ['name', 'voted', 'recent', 'old', 'nofiles']:
        raise Exception("Unrecognized key")

    packages_tuples = []
    for attr in ['name', 'voted', 'recent', 'old', 'nofiles']:
        packages_tuples.append(rdb.sort('packageIds',
                                        by='package:*:%s' % key,
                                        desc=True,
                                        get='package:*:%s' % attr))
    return packages_tuples

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
        rdb.lpush('hw-uuids', hw_uuid)
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
        rdb.lpush('packageIds', package_id)
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
    (r"/post", MainHandler),
    (r"/system/([a-f0-9\-]+)", SystemHandler),
    (r"/submission/([0-9]+)", SubmissionHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
