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

from sqlalchemy import Column, ForeignKey, ForeignKeyConstraint, String

from popcorn.database import Base
from popcorn.models import Distro

class System(Base):
    __tablename__ = 'systems'
    hw_uuid = Column(String(36), primary_key=True)
    distro_name = Column(String(20))
    distro_version = Column(String(10))
    arch = Column(String(10), ForeignKey('arches.name'))
    __table_args__ = (ForeignKeyConstraint([distro_name, distro_version],
                                           [Distro.name, Distro.version]),
                      {})

    def __init__(self, hw_uuid, arch, distro_name, distro_version):
        self.hw_uuid = hw_uuid
        self.arch = arch
        self.distro_name = distro_name
        self.distro_version = distro_version

    def __repr__(self):
        return '<System: %s>' % self.hw_uuid
    
