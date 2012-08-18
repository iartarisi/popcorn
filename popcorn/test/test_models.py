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
                            PackageStatus, SubmissionPackage, Vendor,
                            PackageArchive)


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

        self.db_session = db_session

    def tearDown(self):
        db_session.remove()


class ModelsSimpleTests(ModelsTest):
    def test_system_creation(self):
        self.assertEqual(System.query.all(), [])

        sys = System('hwuuid')
        db_session.add(sys)
        db_session.commit()

        self.assertEqual(System.query.all(), [sys])

    def test_submission_creation(self):
        self.assertEqual(Submission.query.all(), [])

        sub = Submission('openSUSE', '12.1', 'i586', 'POPCORN v0.0.1')
        db_session.add(sub)
        db_session.commit()

        self.assertEqual(Submission.query.all(), [sub])

    def test_submission_foreign_key_constraint(self):
        sub = Submission('bogus', '12.1', 'i586', 'POPCORN v0.0.1')
        db_session.add(sub)

        self.assertRaises(IntegrityError, db_session.commit)

    def test_submission_package_creation(self):
        sub = Submission('openSUSE', '12.1', 'i586', 'POPCORN v0.0.1')
        vendor = Vendor('repo1')

        db_session.add(sub)
        db_session.add(vendor)
        db_session.flush()

        subp = SubmissionPackage(sub.sub_id, date.today(), 'python',
                                 '2.7', '3', '', 'i586', 'repo1', 'voted')
        db_session.add(subp)
        db_session.flush()

        self.assertEqual(SubmissionPackage.query.first(), subp)

    def test_submission_package_no_epoch(self):
        sub = Submission('openSUSE', '12.1', 'i586', 'POPCORN v0.0.1')

    def test_package_archives_foreign_key_constraint(self):
        vendor = Vendor('repo1')
        archive = PackageArchive('firefox', 'v1', 'r1', 'i586', 'dummy',
                                 '12.1', 'vendor', 'voted', date.today(), 1)
        db_session.add(archive)

        self.assertRaises(IntegrityError, db_session.commit)

    def test_package_archive_creation(self):
        vendor = Vendor('repo1')
        archive = PackageArchive('firefox', 'v1', 'r1', 'i586',
                                 'http://repo.url', 'voted', 'openSUSE',
                                 '12.1', date.today(), 1)
        db_session.add(vendor)
        db_session.flush()
        db_session.add(archive)
        db_session.flush()
        self.assertEqual(PackageArchive.query.first(), archive)
