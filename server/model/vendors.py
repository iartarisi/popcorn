from configs import rdb

class Vendor(object):
    """A vendor is the provider of a repository"""
    def __init__(self, name):
        """
        Retrieves or creates a Vendor object.

        :name: A string that identifies this vendor

        """
        self.name = name
        self.key = _normalize_vendor(name)
        try:
            rdb['vendor:%s' % self.key]
        except KeyError:
            self.id = str(rdb.incr('global:nextVendorId'))
            rdb.set('vendor:%s', self.key, name)
            rdb.sadd('vendors', self.key)

def _normalize_vendor(vendor_name):
    # redis keys cannot contain spaces
    return vendor_name.replace(' ', '_')
