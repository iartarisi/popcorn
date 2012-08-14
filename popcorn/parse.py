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

"""Parse the submissions received from the clients and save them to the DB"""

from datetime import date

from sqlalchemy.exc import DataError
from sqlalchemy.orm.exc import NoResultFound

from popcorn.configs import SUBMISSION_INTERVAL
from popcorn.database import db_session
from popcorn.models import (Arch, Distro, SubmissionPackage, Submission,
                            System, Vendor)


class FormatError(Exception):
    """Exception class for format errors found in a submission"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "The submission format is invalid: %s" % self.message


class EarlySubmissionError(Exception):
    """Raised when another Submission has been submitted too soon for a
    System
    """
    def __init__(self, last_date):
        self.last_date = last_date

    def __str__(self):
        return ("You need to wait %s days between submissions. "
                "Your last recorded submission was on %s."
                % (SUBMISSION_INTERVAL, self.last_date))


def parse_text(data):
    """Parse a plaintext submission, recording everything in the database"""
    datalines = data.splitlines()
    (popcorn, version, distro, distrover, arch, subid) = datalines[0].split()

    try:  # TEST THIS
        system = System.query.filter_by(submission_id=subid).one()
    except NoResultFound:
        system = System(subid, arch, distro, distrover)
        try:
            Arch.query.filter_by(arch=arch).one()
        except NoResultFound:
            raise FormatError("unknown arch - " + arch)

        try:
            Distro.query.filter_by(distro_name=distro,
                                   distro_version=distrover).one()
        except NoResultFound:
            distro = Distro(distro, distrover)
            db_session.add(distro)
        db_session.add(system)

    # TODO: think about moving this to the model
    if not _can_submit(system):
        raise EarlySubmissionError(system.last_submission.sub_date)

    today = date.today()
    sub = Submission(system.submission_id, version, today)
    db_session.add(sub)
    for line in datalines[1:]:
        try:
            (status, name, version, release,
             epoch, arch, vendor) = line.split(None, 6)
        except ValueError, e:  # test this
            raise FormatError(e.message)

        try:
            status = {'v': 'voted',
                      'r': 'recent',
                      'o': 'old',
                      'n': 'nofiles'}[status]
        except KeyError:
            raise FormatError("the package's status could not be recognized")

        try:
            vendor = Vendor.query.filter_by(vendor_name=vendor[:20]).one()
        except NoResultFound:
            vendor = Vendor(vendor)
            db_session.add(vendor)
            try:
                db_session.flush()
            except DataError:  # TODO mail this to the admins
                raise

        sp = SubmissionPackage(subid, today, name, version, release,
                               epoch, arch, vendor.vendor_name, status)
        db_session.add(sp)

    try:
        db_session.commit()
    except DataError:  # TODO mail this to the admins
        raise


def _can_submit(system):
    """Checks the Submission interval for this System

    :system: a System object

    If the interval has elapsed or there are no previous submissions, it
    will return True, otherwise returns False.

    """
    last_sub = system.last_submission
    if not last_sub:
        return True
    delta = date.today() - last_sub.sub_date
    if SUBMISSION_INTERVAL < delta.days:
        return True
    else:
        return False
