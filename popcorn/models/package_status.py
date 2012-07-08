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

from sqlalchemy import Column, String

from popcorn.database import Base


class PackageStatus(Base):
    """The Package Status in a submission. Can be one of:

    * (r) recent
    - package has been recently installed (less than 30 days)

    * (v) voted
    - package is older than 30 days and has been used in the last 30 days
    - ( now - install_time > 30 days ) and ( now - access_time < 30 days)

    * (o) old
    - package is older than 30 days and hasn't been used recently
    - ( now - install_time > 30 days ) and ( now - access_time > 30 days)

    * (n) no-files
    - there are no watched files present in the package
    - access_time = 0

    """
    __tablename__ = 'package_statuses'
    pkg_status = Column(String(10), primary_key=True)
    short_status = Column(String(1), unique=True)

    def __init__(self, pkg_status):
        # TODO: disable this after creating the initial statuses in a script
        self.pkg_status = pkg_status
        self.short_status = pkg_status[0]

    def __repr__(self):
        return '<PackageStatus: %s(%s)>' % (self.pkg_status, self.short_status)

    @property
    def _flat_attrs(self):
        return {
            'pkg_status': self.pkg_status,
            'short_status': self.short_status,
        }

    @property
    def serialize(self):
        return dict(**self._flat_attrs)
