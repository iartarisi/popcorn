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

import unittest

import redis

from popcorn import configs
configs.rdb = rdb = redis.Redis('localhost', db='13')
from popcorn.model import Distro, System

class TestSystems(unittest.TestCase):
    def setUp(self):
        self.distro = Distro('Foo', '0.0')

    def tearDown(self):
        rdb.flushdb()

    def test_init_system_attributes(self):
        s = System('sysid', 'Foo', '0.0', 'i586')
        self.assertEqual(
            (s.id, s.arch, str(s.distro)),
            ('1', 'i586', str(self.distro)))

    def test_last_submission_none(self):
        s = System('sysid', 'Foo', '0.0', 'i586')
        self.assertIsNone(s.last_submission)
