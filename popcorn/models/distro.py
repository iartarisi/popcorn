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
from sqlalchemy.orm import relationship

from popcorn.database import Base


class Distro(Base):
    __tablename__ = 'distros'
    distro_name = Column(String(20), primary_key=True)
    distro_version = Column(String(10), primary_key=True)
    systems = relationship('System')

    def __init__(self, distro_name, distro_version):
        self.distro_name = distro_name
        self.distro_version = distro_version

    def __repr__(self):
        return "<Distro: %s %s>" % (self.distro_name, self.distro_version)

    @property
    def _flat_attrs(self):
        return {
            'distro_name': self.distro_name,
            'distro_version': self.distro_version,
        }

    @property
    def serialize(self):
        return dict({'systems': [sys._flat_attrs for sys in self.systems]},
                    **self._flat_attrs)
