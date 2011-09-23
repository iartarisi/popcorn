from configs import rdb

class System(object):
    """A system is a user machine that we want to track."""

    # XXX think about memoizing the objects in this class, so they don't
    # get created every time we need to look for one
    def __init__(self, hw_uuid, arch):
        """Check if the system is in our database and create it if it isn't

        :arg hw-uuid: smolt hw-uuid to uniquely indentify each system
        """
        key = 'hw-uuid:%s' % hw_uuid
        try:
            self.id = rdb[key]
        except KeyError:
            self.id = str(rdb.incr('global:nextSystemId'))
            rdb.lpush('hw-uuids', hw_uuid)
            rdb[key] = self.id

            # XXX see if this constraint can go in the database,
            # otherwise just make it prettier
            assert arch in ['i586', 'x86_64']
            rdb.set('system:%s:arch' % self.id, arch)
