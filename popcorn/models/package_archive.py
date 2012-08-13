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

from sqlalchemy import (Column, ForeignKey, String, Integer,
                        ForeignKeyConstraint)

from popcorn.database import Base
from popcorn.models import Distro


class PackageArchive(Base):
    __tablename__ = 'package_archives'

    pkg_name = Column(String(50), primary_key=True)
    pkg_version = Column(String(50), primary_key=True)
    pkg_release = Column(String(50), primary_key=True)
    pkg_arch = Column(String(10), ForeignKey('arches.arch'), primary_key=True)
    distro_name = Column(String(20), ForeignKey('distros.distro_name'),
            primary_key=True)
    distro_version = Column(String(20),
            ForeignKey('distros.distro_version'), primary_key=True)
    vendor_name = Column(String(20), ForeignKey('vendors.vendor_name'),
            primary_key=True),
    pkg_status = Column(String(10), ForeignKey('package_statuses.pkg_status'),
                        primary_key=True)
    month = Column(String(10), primary_key=True)
    count = Column(Integer)

    __table_args__ = (
        ForeignKeyConstraint(
            [distro_name, distro_version],
            [Distro.distro_name, Distro.distro_version]
            ),
        )

    def __init__(self, pkg_name, pkg_version, pkg_release, pkg_arch,
                 distro_name, distro_version, vendor_name, pkg_status, month,
                 count):
        self.pkg_name = pkg_name
        self.pkg_version = pkg_version
        self.pkg_release = pkg_release
        self.pkg_arch = pkg_arch
        self.distro_name = distro_name
        self.distro_version = distro_version
        self.vendor_name = vendor_name
        self.pkg_status = pkg_status
        self.month = month
        self.count = count

    def __repr__(self):
        output = ("<PackageArchive: %(name)s-%(ver)s-%(rel)s.%(arch)s"
                  "%(distro_name)s %(distro_version)s - %(status)s"
                  "count: %(count)s %(month)s")
        return output % dict(name=self.pkg_name,
                             ver=self.pkg_version,
                             rel=self.pkg_release,
                             arch=self.pkg_arch,
                             status=self.pkg_status,
                             **self.__dict__)
