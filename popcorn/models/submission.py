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

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from popcorn.database import Base

class Submission(Base):
    __tablename__ = 'submissions'
    date = Column(DateTime(), primary_key=True)
    system_hw_uuid = Column(String(36), ForeignKey('systems.hw_uuid'),
                            primary_key=True)
    popcorn_version = Column(String(30), nullable=False)

    def __init__(self, date, system_hw_uuid, popcorn_version):
        self.date = date
        self.system_hw_uuid = system_hw_uuid
        self.popcorn_version = popcorn_version

    def __repr__(self):
        return '<Submission from %s at %s>' % (self.system_hw_uuid, self.date)
