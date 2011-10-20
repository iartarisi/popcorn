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

from datetime import datetime

from popcorn.configs import submission_interval, rdb
from popcorn.model import Package, Submission, System, Vendor

"""Functionality for parsing the submissions received from the clients"""

class FormatError(Exception):
    """Exception class for format errors found in a submission"""
    def __init__(self, message):
        self.message = message
    def __str__(self, message):
        return "The submission format is invalid: %s" % self.message

class EarlySubmission(Exception):
    """Raised when another Submission has been submitted too soon for a System"""
    pass

def parse_text(data):
    """Parse a plaintext submission, recording everything in the database"""
    datalines = data.splitlines()
    (popcorn, version, distro, distrover, arch, hw_uuid) = datalines[0].split()

    system = System(hw_uuid, distro, distrover, arch)
    
    if not _can_submit(system):
        raise EarlySubmission

    sub = Submission(system, version)
    for line in datalines[1:]:
        (status, name, version, release,
         epoch, arch, vendor) = line.split(None, 6)
        assert status in ['v', 'r', 'o', 'n'], FormatError(
            "the package's status could not be recognized")
        vendor = Vendor(vendor)
        package = Package(name, version, release, epoch,
                          arch, vendor, status, sub)
    rdb.save()

def _can_submit(system):
    """Checks the Submission interval for this System

    :system: a System object

    If the interval has elapsed or there are no previous submissions, it
    will return True, otherwise returns False.

    """
    last_sub = system.last_submission
    if not last_sub:
        return True
    delta = datetime.now() - last_sub.datetime
    if submission_interval < delta.days:
        return True
    else:
        return False
