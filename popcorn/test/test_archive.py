# -*- coding: utf-8 -*-
# Copyright (c) 2012 Akshit Khurana <axitkhurana@gmail.com>
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

from datetime import date, timedelta

from popcorn.archive import update_archives
from popcorn.models import (System, Submission, SubmissionPackage,
                            PackageArchive)
from popcorn.database import db_session
from popcorn.test.test_models import ModelsTest


class TestArchivePackages(ModelsTest):
    def setUp(self):
        super(TestArchivePackages, self).setUp()
        self.old_date = date.today() - timedelta(days=400)
        self.today = date.today()

        s1 = System('i586', 'Fedora', '16')
        db_session.add(s1)
        db_session.flush()
        sub1 = Submission(s1.submission_id, 'v1', self.old_date)
        subp1 = SubmissionPackage(s1.submission_id, self.old_date, 'python',
                                  '2.7', '3', '', 'i586', 'http://repo.url',
                                  'voted')
        subp2 = SubmissionPackage(s1.submission_id, self.old_date, 'chrome',
                                  '2.7', '3', '', 'i586', 'http://repo.url',
                                  'voted')
        db_session.add(sub1)
        db_session.flush()
        db_session.add_all([subp1, subp2])
        db_session.flush()
        update_archives(self.old_date)

    def test_archive_package_month(self):
        self.assertEqual(len(PackageArchive.query.all()), 2)
        month = PackageArchive.query.filter_by(pkg_name='python').one().month
        self.assertEqual(month, self.old_date.replace(day=1))

    def test_archive_package_count(self):
        s2 = System('i586', 'Fedora', '16')
        db_session.add(s2)
        db_session.flush()

        sub2 = Submission(s2.submission_id, 'v1', self.today)
        subp3 = SubmissionPackage(s2.submission_id, self.today, 'python',
                                  '2.7', '3', '', 'i586', 'http://repo.url',
                                  'voted')
        subp4 = SubmissionPackage(s2.submission_id, self.today, 'chrome',
                                  '2.7', '3', '', 'i586', 'http://repo.url',
                                  'voted')
        db_session.add(sub2)
        db_session.flush()
        db_session.add_all([subp3, subp4])
        db_session.flush()

        s3 = System('i586', 'Fedora', '16')
        db_session.add(s3)
        db_session.flush()

        sub3 = Submission(s3.submission_id, 'v1', self.today)
        subp5 = SubmissionPackage(s3.submission_id, self.today, 'python',
                                  '2.7', '3', '', 'i586', 'http://repo.url',
                                  'voted')

        db_session.add(sub3)
        db_session.flush()

        db_session.add(subp5)
        db_session.flush()

        update_archives(date.today())

        self.assertEqual(len(PackageArchive.query.all()), 4)

        query = PackageArchive.query.filter_by(pkg_name='python',
                                               month=self.today.replace(day=1))
        count = self.assertEqual(query.one().count, 2)
