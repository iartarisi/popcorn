from configs import rdb

class Package(object):
    """A package object"""
    def __init__(self, name, version, release, arch, vendor):
        """Get or create a package object"""
        self.name = name
        self.version = version
        self.release = release
        self.arch = arch
        self.vendor = vendor
        key = 'packageId:%(name)s:%(ver)s:%(rel)s:%(arch)s:%(vendor)s' % locals()
        try:
            self.id = rdb[key]
        except KeyError:
            self.id = str(rdb.incr('global:nextPackageId'))
            rdb[key] = self.id
            rdb.lpush('packageIds', package_id)
            rdb.hset("package:%s" % self.id, 'name', self.name)
            rdb.sadd("vendor:%s:packages" % vendor, self.id)

    @classmethod
    def find(id):
        key = 
