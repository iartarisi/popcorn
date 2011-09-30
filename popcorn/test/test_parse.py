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
from popcorn.parse import parse_text


class TestParsePopcorn(unittest.TestCase):
    def test_parse_popcorn_success(self):
        submission = ("POPCORN 0.1 x86_64 TEST_HW_UUID\n"
                      "v python 2.5 1.1 None x86_64 http://repo.url\n"
                      "o python-lint 1.1 1 None noarch http://repo.url\n")
        parse_text(submission)
        self.assertEqual(rdb.get('global:nextSubmissionId'), '1')
        self.assertEqual(rdb.get('global:nextSystemId'), '1')
        self.assertEqual(rdb.get('global:nextPackageId'), '2')
        self.assertEqual(rdb.get(
            'vendor:1:package:python-2.5-1.1.x86_64'), '1')
        self.assertEqual(rdb.get(
            'vendor:1:package:python-lint-1.1-1.noarch'), '2')
        self.assertEqual(rdb.hget('package:1:status', 'voted'), '1')
        self.assertEqual(rdb.hget('package:2:status', 'old'), '1')

        self.assertEqual(rdb.smembers('vendors'), set(['1']))
        self.assertEqual(rdb.smembers('vendor:1:packages'),
                         set(['1', '2']))
        self.assertEqual(rdb.smembers('systems'), set(['TEST_HW_UUID']))
        self.assertEqual(rdb.smembers('system:1:submissions'), set(['1']))

    def tearDown(self):
        rdb.flushdb()
