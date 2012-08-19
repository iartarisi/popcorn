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

from datetime import date

from sqlalchemy import Column, Date, String

from popcorn.database import Base


class UniqueSystem(Base):
    __tablename__ = 'unique_systems'
    sys_hwuuid = Column(String(64), primary_key=True)
    sub_date = Column(Date())

    def __init__(self, sys_hwuuid, date=date.today()):
        self.sys_hwuuid = sys_hwuuid
        self.sub_date = date

    def __repr__(self):
        return '<Unique System %s: Last submission at %s>' % (self.sys_hwuuid,
                                                              self.sub_date)

    @property
    def _flat_attrs(self):
        return {
            'sys_hwuuid': self.sys_hwuuid,
            'sub_date': self.sub_date.strftime("%Y-%m-%d"),
        }

    @property
    def serialize(self):
        return dict(**self._flat_attrs)
