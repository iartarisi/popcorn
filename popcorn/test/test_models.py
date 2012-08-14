# -*- coding: utf-8 -*-
# Copyright (c) 2012 Ionuț Arțăriși <iartarisi@suse.cz>
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

"""Glue tests to ensure relationships between tables and other constraints"""

from datetime import date, timedelta
import sys
import unittest

from sqlalchemy import create_engine, event
from sqlalchemy.exc import IntegrityError

from popcorn.database import db_session, Base
from popcorn.models import (Arch, Distro, System, Submission,
                            PackageStatus, SubmissionPackage, Vendor)


# we need to explicitly enable foreign key constraints for sqlite
def _fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute('pragma foreign_keys=ON')


class ModelsTest(unittest.TestCase):

    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        # engine = create_engine('sqlite:///test.db')

        event.listen(engine, 'connect', _fk_pragma_on_connect)
        db_session.configure(bind=engine)

        Base.metadata.create_all(bind=engine)

        db_session.add_all([Arch('i586'), Arch('x86_64'), Arch('noarch')])
        db_session.add_all([Distro('Fedora', '16'),
                           Distro('openSUSE', '12.1')])
        db_session.add_all([PackageStatus('voted'), PackageStatus('recent'),
                            PackageStatus('no-files'), PackageStatus('old')])
        db_session.add(Vendor('http://repo.url'))
        db_session.flush()

        # system is dependent on both arches and distros already being
        # in the db
        db_session.add_all([System('subid1', 'i586', 'Fedora', '16'),
                            System('subid2', 'i586', 'openSUSE', '12.1')])
        db_session.commit()

        self.db_session = db_session

    def tearDown(self):
        db_session.remove()


class ModelsSimpleTests(ModelsTest):
    def test_system_foreign_key_constraint(self):
        db_session.add(System('hw_uu', 'i586', 'bogus', 'bogus'))

        self.assertRaises(IntegrityError, db_session.flush)
        db_session.rollback()

        db_session.add(System('hw_uu', 'bogus', 'Fedora', '16'))
        self.assertRaises(IntegrityError, db_session.flush)

    def test_submission_creation(self):
        sub = Submission('subid1', 'POPCORN v0.0.1')

        s1 = System.query.first()
        self.assertEqual(s1.submissions, [])

        db_session.add(sub)
        db_session.commit()

        self.assertEqual(Submission.query.all(), [sub])
        self.assertEqual(s1.submissions, [sub])

    def test_submission_foreign_key_constraint(self):
        sub = Submission('bogus', 'POPCORN v0.0.1')
        db_session.add(sub)

        self.assertRaises(IntegrityError, db_session.commit)

    def test_submission_package_creation(self):
        sub = Submission('subid1', 'POPCORN v0.0.1')
        vendor = Vendor('repo1')
        subp = SubmissionPackage('subid1', date.today(), 'python', '2.7',
                                 '3', '', 'i586', 'repo1', 'voted')
        db_session.add(sub)
        db_session.add(vendor)
        db_session.flush()
        db_session.add(subp)
        db_session.flush()

        self.assertEqual(SubmissionPackage.query.first(), subp)

    def test_system_last_submission(self):
        sub1 = Submission('subid1', 'P1', date.today())
        sub2 = Submission('subid2', 'P1',
                          date.today() - timedelta(days=31 * 2))
        sub3 = Submission('subid1', 'P1',
                          date.today() - timedelta(days=31 * 3))
        s1 = System.query.first()
        self.assertIsNone(s1.last_submission)

        db_session.add_all([sub1, sub2, sub3])
        db_session.commit()

        self.assertEqual([sub1, sub3], s1.submissions)
        self.assertEqual(sub1, s1.last_submission)

    def test_submission_package_no_epoch(self):
        sub = Submission("subid1", "P1", date.today())
