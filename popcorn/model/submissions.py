from datetime import date

from popcorn.configs import rdb

class Submission(object):
    """A set of data from a system captured at a specific time."""

    @classmethod
    def find(self, sub_id):
        """Return an existing submission"""
        raise NotImplementedError()

    def __init__(self, system, version=None):
        """
        :system: a System object that this submission was sent from
        :version: a string with the Popcorn version that sent this submission

        """
        self.system = system

        # create new submission
        self.id = str(rdb.incr('global:nextSubmissionId'))
        self.date = date.today().strftime('%y-%m-%d')
        rdb.set('submission:%s:date' % system.id, self.date)

        # attach submission to system
        rdb.lpush('system:%s:submissions' % self.id, self.id)

        # record version
        rdb.set('submission:%s:popcorn' % self.id, version)

    def add_package(self, package):
        """Add a Package to this submission"""
        rdb.lpush("submission:%s:packages" % self.id, package.id)
