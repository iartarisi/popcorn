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

from sqlalchemy import Column, ForeignKey, String

from popcorn.database import Base

class Package(Base):
    __tablename__ = 'packages'
    name = Column(String(50), primary_key=True)
    version = Column(String(20), primary_key=True)
    release = Column(String(10), primary_key=True)
    epoch = Column(String(10), primary_key=True)
    arch = Column(String(10), ForeignKey('arches.name'), primary_key=True)
    vendor_name = Column(String(20), ForeignKey('vendors.name'),
                         primary_key=True)

    def __init__(self, name, version, release, epoch, arch, vendor_name):
        self.name = name
        self.version = version
        self.release = release
        self.epoch = epoch
        self.arch = arch
        self.vendor_name = vendor_name

    def __repr__(self):
        if self.epoch:
            return ('<Package %(name)s-%(release)s-%(epoch)s.%(arch)s '
                    'from %(vendor_name)s' % self.__dict__)
        else:
            return ('<Package %(name)s-%(release)s.%(arch)s '
                    'from %(vendor_name)s' % self.__dict__)
        
