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

from sqlalchemy import (Column, Date, ForeignKey, ForeignKeyConstraint,
                        String, Integer)
from sqlalchemy.orm import relationship

from popcorn.database import Base
from popcorn.models import Submission


class SubmissionPackage(Base):
    __tablename__ = 'submission_packages'

    # primary key
    submission_id = Column(Integer, ForeignKey('systems.submission_id'),
                        primary_key=True,)
    sub_date = Column(Date(), primary_key=True)
    pkg_name = Column(String(50), primary_key=True)
    pkg_version = Column(String(50), primary_key=True)
    pkg_release = Column(String(50), primary_key=True)
    pkg_epoch = Column(String(10), primary_key=True)
    pkg_arch = Column(String(10), ForeignKey('arches.arch'), primary_key=True)
    vendor_name = Column(String(20), ForeignKey('vendors.vendor_name'),
                         primary_key=True)
    # not primary key
    pkg_status = Column(String(10), ForeignKey('package_statuses.pkg_status'),
                        nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            [submission_id, sub_date],
            [Submission.submission_id, Submission.sub_date]
            ),
        )

    def __init__(self, submission_id, sub_date, pkg_name, pkg_version,
                 pkg_release, pkg_epoch, pkg_arch, vendor_name, pkg_status):
        self.submission_id = submission_id
        self.sub_date = sub_date
        self.pkg_name = pkg_name
        self.pkg_version = pkg_version
        self.pkg_release = pkg_release
        self.pkg_epoch = pkg_epoch if pkg_epoch != "None" else ""
        self.pkg_arch = pkg_arch
        self.vendor_name = vendor_name
        self.pkg_status = pkg_status

    def __repr__(self):
        if self.pkg_epoch:
            output = ("<SubmissionPackage: %(submission_id)s %(sub_date)s "
                      "%(name)s-%(ver)s-%(rel)s-%(epoch)s.%(arch)s - "
                      "%(status)s")
        else:
            output = ("<SubmissionPackage: %(submission_id)s %(sub_date)s "
                      "%(name)s-%(ver)s-%(rel)s.%(arch)s - %(status)s")
        return output % dict(name=self.pkg_name,
                             ver=self.pkg_version,
                             rel=self.pkg_release,
                             epoch=self.pkg_epoch,
                             arch=self.pkg_arch,
                             status=self.pkg_status,
                             **self.__dict__)

    @property
    def nvrea(self):
        if self.pkg_epoch:
            nvrea = "%(name)s-%(ver)s-%(rel)s-%(epoch)s.%(arch)s"
        else:
            nvrea = "%(name)s-%(ver)s-%(rel)s.%(arch)s"

        return nvrea % dict(name=self.pkg_name,
                            ver=self.pkg_version,
                            rel=self.pkg_release,
                            epoch=self.pkg_epoch,
                            arch=self.pkg_arch)

    @property
    def _flat_attrs(self):
        return {
            'submission_id': self.submission_id,
            'sub_date': self.sub_date.strftime("%Y-%m-%d"),
            'pkg_name': self.pkg_name,
            'pkg_version': self.pkg_version,
            'pkg_release': self.pkg_release,
            'pkg_epoch': self.pkg_epoch,
            'pkg_arch': self.pkg_arch,
            'vendor_name': self.vendor_name,
            'pkg_status': self.pkg_status,
        }

    @property
    def serialize(self):
        return dict(**self._flat_attrs)
