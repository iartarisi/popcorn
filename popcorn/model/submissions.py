# -*- coding: utf-8 -*-
# Copyright (c) 2011 Ionuț Arțăriși <iartarisi@suse.cz>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

from datetime import date

from popcorn.configs import rdb
from popcorn.model.utils import list_to_tuples

class Submission(object):
    """A set of data from a system captured at a specific time.

    A submission is identified by its id. The id is incremented in
    'global:nextSubmissionId'.

    A new submission is created every time a client system submits a
    full popcorn set of data if the interval between the last submission
    is greater than the accepted interval defined in the configuration
    file under app.submission_interval (the default is 30 days).

    Information about submissions are stored in a hash at
    'submission:%(id)s'. The keys are:
       - date - when this submission was created
       - popcorn - the name/version of the client application.

    Submissions belong to a system and their ids are stored in the set
    at 'system:%s:submissions'.

    """
    @classmethod
    def find(cls, sub_id):
        """Return an existing Submission by id"""
        date, popcorn = rdb.hmget('submission:%s' % sub_id, ['date', 'popcorn'])
        if None in (date, popcorn):
            raise DoesNotExist('Submission', sub_id)

        obj = cls.__new__(cls)
        obj.__dict__.update(date=date, popcorn=popcorn, id=str(sub_id))
        return obj

    def __init__(self, system, popcorn=None):
        """Create a new submission

        :system: a System object that this submission was sent from
        :popcorn: a string with the Popcorn version that sent this submission

        """
        self.system = system

        # TODO check time interval from last submission
        # create new submission
        self.id = str(rdb.incr('global:nextSubmissionId'))
        self.date = date.today().strftime('%d-%m-%y')
        self.popcorn = popcorn

        rdb.hmset('submission:%s' % self.id, {'date': self.date,
                                              'popcorn': popcorn})
        # attach submission to system
        rdb.sadd('system:%s:submissions' % self.system.id, self.id)

    def add_package(self, package):
        """Add a Package to this submission"""
        rdb.sadd("submission:%s:packages" % self.id, package.id)

    def __repr__(self):
        return "<Submissions %s from %s>" % (self.id, self.date)

    def get_package_names_with_status(self):
        """Return a list of tuples of the form (id, package-name, status)"""
        # get the set sorted by name (Nvrea)
        alist  = rdb.sort('submission:%s:packages' % self.id,
                          by='package:*:nvrea', alpha=True,
                          get=['#', 'package:*:nvrea',
                               'submission:%s:package:*:status' % self.id])
        return list_to_tuples(alist, 3)
