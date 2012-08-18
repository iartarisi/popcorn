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

from datetime import date

from sqlalchemy import Column, Date, ForeignKey, String, Integer
from sqlalchemy.orm import relationship

from popcorn.database import Base


class SubmissionError(Exception):
    pass


class Submission(Base):
    __tablename__ = 'submissions'
    sub_date = Column(Date(), primary_key=True)
    submission_id = Column(Integer, ForeignKey('systems.submission_id'),
                        primary_key=True)
    popcorn_version = Column(String(30), nullable=False)

    submission_packages = relationship('SubmissionPackage')

    def __init__(self, submission_id, popcorn_version, date=date.today()):
        self.sub_date = date
        self.submission_id = submission_id
        self.popcorn_version = popcorn_version

    def __repr__(self):
        return '<Submission from %s at %s>' % (self.submission_id,
                                               self.sub_date)

    @property
    def _flat_attrs(self):
        return {
            'sub_date': self.sub_date.strftime("%Y-%m-%d"),
            'submission_id': self.submission_id,
            'popcorn_version': self.popcorn_version,
        }

    @property
    def serialize(self):
        return dict({'submission_packages': [sub._flat_attrs for sub in
                    self.submission_packages]}, **self._flat_attrs)
