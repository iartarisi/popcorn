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

from sqlalchemy import (Column, ForeignKey, ForeignKeyConstraint, String,
                        Integer)
from sqlalchemy.orm import relationship

from popcorn.database import Base
from popcorn.models import Distro, Submission


class System(Base):
    __tablename__ = 'systems'
    submission_id = Column(Integer, primary_key=True, autoincrement=True)
    distro_name = Column(String(20), nullable=False)
    distro_version = Column(String(10), nullable=False)
    arch = Column(String(10), ForeignKey('arches.arch'), nullable=False)

    submissions = relationship('Submission', backref='system',
                               order_by=Submission.sub_date.desc())

    __table_args__ = (
        ForeignKeyConstraint([distro_name, distro_version],
                             [Distro.distro_name, Distro.distro_version]),
        {})

    def __init__(self, arch, distro_name, distro_version):
        self.arch = arch
        self.distro_name = distro_name
        self.distro_version = distro_version

    def __repr__(self):
        return "<System: %s>" % self.submission_id

    @property
    def last_submission(self):
        return Submission.query.filter_by(
                submission_id=self.submission_id).order_by(
                Submission.sub_date.desc()).first()

    @property
    def _flat_attrs(self):
        return {
            'submission_id': self.submission_id,
            'distro_name': self.distro_name,
            'distro_version': self.distro_version,
            'arch': self.arch,
        }

    @property
    def serialize(self):
        return dict({'submissions': [sub._flat_attrs for sub in
                    self.submissions]}, **self._flat_attrs)
