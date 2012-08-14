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

from datetime import date, timedelta

from sqlalchemy.orm.exc import NoResultFound

from popcorn.parse import (parse_text, _can_submit, EarlySubmissionError,
                           FormatError)
from popcorn.models import (Distro, System, Submission, SubmissionPackage,
                            Vendor)

from popcorn.test.test_models import ModelsTest


class TestParsePopcorn(ModelsTest):
    def test_parse_popcorn_success(self):
        self.assertEqual(System.query.filter_by(submission_id='TEST_SUBID'
                                                ).count(), 0)
        self.assertEqual(SubmissionPackage.query.all(), [])
        subm_text = ("POPCORN 0.1 openSUSE 12.1 i586 TEST_SUBID\n"
                     "v python 2.5 1.1 None x86_64 http://repo.url\n"
                     "o python-lint 1.1 1 None noarch http://repo.url\n")
        parse_text(subm_text)

        system = System.query.filter_by(submission_id='TEST_SUBID').one()

        self.assertEqual(len(system.submissions), 1)

        sub = system.last_submission
        self.assertEqual(len(sub.submission_packages), 2)
        self.assertEqual(SubmissionPackage.query.count(), 2)
        self.assertEqual(Vendor.query.first().vendor_name, "http://repo.url")

        p1 = SubmissionPackage.query.filter_by(pkg_name="python").one()
        self.assertEqual(p1.pkg_name, "python")
        self.assertEqual(p1.pkg_version, "2.5")
        self.assertEqual(p1.pkg_release, "1.1")
        self.assertEqual(p1.pkg_epoch, "")
        self.assertEqual(p1.pkg_arch, "x86_64")
        self.assertEqual(p1.pkg_status, "voted")

    def test_parse_unknown_arch_error(self):
        subm_text = ("POPCORN 0.1 Fedora 12 unknown-arch TEST_SUBID\n")

        self.assertRaises(FormatError, parse_text, subm_text)

    def test_parse_early_submission_error(self):
        system = System.query.first()

        sub = Submission(system.submission_id, '0.1', date.today())
        self.db_session.add(sub)
        self.db_session.commit()
        self.assertEqual(system.submissions, [sub])

        submission = ("POPCORN 0.1 openSUSE 11.4 x86_64 %s\n"
                      % system.submission_id)

        self.assertRaises(EarlySubmissionError, parse_text, submission)
        self.assertEqual(system.submissions, [sub])

    def test_parse_distro_doesnt_exist_gets_created(self):
        self.assertRaises(NoResultFound,
                          Distro.query.filter_by(distro_name="new_Distro").one)

        parse_text("POPCORN 0.1 Distroxillix 1.0 x86_64 some_hwwuid\n")

        distro = Distro.query.filter_by(distro_name="Distroxillix").one()

        self.assertEqual("Distroxillix", distro.distro_name)
        self.assertEqual("1.0", distro.distro_version)


class TestCanSubmit(ModelsTest):
    def test_can_submit(self):
        system = System.query.first()

        # make a submission 400 days ago
        sub1 = Submission(system.submission_id, 'POPCORN1',
                          date.today() - timedelta(days=400))
        self.db_session.add(sub1)
        self.db_session.commit()
        self.assertEqual(system.last_submission, sub1)

        self.assertTrue(_can_submit(system))

    def test_can_submit_no_last_submission(self):
        system = System.query.first()

        self.assertIsNone(system.last_submission)
        self.assertTrue(_can_submit(system))

    def test_can_submit_too_early(self):
        system = System.query.first()

        # 1 day ago should be too early for another submission
        sub1 = Submission(system.submission_id, 'POPCORN 1',
                          date.today() - timedelta(1))
        self.db_session.add(sub1)
        self.db_session.commit()
        self.assertEqual(system.last_submission, sub1)

        self.assertFalse(_can_submit(system))
