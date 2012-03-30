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

import os
import sys
import gzip
import cStringIO
if sys.version >= '2.7':
    import unittest
else:
    import unittest2 as unittest

from sqlalchemy import create_engine, event

from popcorn import app
from popcorn.database import db_session, Base
from popcorn.models import Arch, PackageStatus


# we need to explicitly enable foreign key constraints for sqlite
def _fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute('pragma foreign_keys=ON')


class PopcornTestCase(unittest.TestCase):

    def setUp(self):
        engine = create_engine('sqlite:///:memory:')

        event.listen(engine, 'connect', _fk_pragma_on_connect)
        db_session.configure(bind=engine)

        Base.metadata.create_all(bind=engine)

        self.init_db()
        self.db_session = db_session
        self.app = app.test_client()

    def tearDown(self):
        db_session.remove()

    def init_db(self):
        db_session.add_all([Arch('noarch'), Arch('i586'), Arch('i686'),
                            Arch('i486'), Arch('i386'), Arch('x86_64'),
                            Arch('ppc'), Arch('ppc64'), Arch('s390'),
                            PackageStatus('voted'), PackageStatus('nofiles'),
                            PackageStatus('recent'), PackageStatus('old')])
        db_session.commit()

    def submit(self, compress, header):
        submission_file = os.path.join(os.path.dirname(__file__), 'fixtures',
                                       'submission-suse.txt')
        f_in = open(submission_file, 'rb')
        if compress:
            f = cStringIO.StringIO()
            g = gzip.GzipFile(mode='wb',  fileobj=f)
            g.writelines(f_in)
            g.close()
            f_in.close()
            f.seek(0)
        else:
            f = f_in
        if header:
            return self.app.post('/', data=dict(popcorn=(f, 'popcorn.txt.gz')),
                    headers={'Content-Encoding': 'gzip', })
        else:
            return self.app.post('/', data=dict(popcorn=(f, 'popcorn.txt')))

    def test_submission_gzip_with_header(self):
        rv = self.submit(compress=True, header=True)
        self.assertEqual('Submission received. Thanks!', rv.data)

    def test_submission_plaintext_with_header(self):
        rv = self.submit(compress=False, header=True)
        self.assertEqual('Submission received. Thanks!', rv.data)

    def test_submission_plaintext_without_header(self):
        rv = self.submit(compress=False, header=False)
        self.assertEqual('Submission received. Thanks!', rv.data)
