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
from popcorn.model import Distro, Package, Vendor, System, Submission


class TestPackages(unittest.TestCase):

    def setUp(self):
        self.distro = Distro('Foo', '0.0')

    def test_init_package_attributes(self):
        ven = Vendor('v')
        sys = System('sysid', 'Foo', '0.0', 'i586')
        sub = Submission(sys, 'popver')
        p = Package('name', 'ver', 'rel', 'ep', 'arch', ven, 'o', sub)
        self.assertTupleEqual(
            (p.name, p.version, p.release, p.epoch, p.arch, p.vendor, p.status, p.sub.__class__),
            ('name', 'ver', 'rel', 'ep', 'arch', ven, 'old', Submission))

    def test_init_package_status_old(self):
        vendor = Vendor('v')
        sys = System('sysid', 'Foo', '0.0', 'i586')
        Package('name', 'ver', 'rel', 'ep', 'arch', vendor, 'o', sys)
        p = Package('name', 'ver', 'rel', 'ep', 'arch', vendor, 'o', sys)
        self.assertEqual(p.old, '2')

    def test_init_package_status_recent(self):
        vendor = Vendor('v')
        sys = System('sysid', 'Foo', '0.0', 'i586')
        Package('name', 'ver', 'rel', 'ep', 'arch', vendor, 'r', sys)
        p = Package('name', 'ver', 'rel', 'ep', 'arch', vendor, 'r', sys)
        self.assertEqual(p.recent, '2')

    def test_init_package_status_nofiles(self):
        vendor = Vendor('v')
        sys = System('sysid', 'Foo', '0.0', 'i586')
        Package('name', 'ver', 'rel', 'ep', 'arch', vendor, 'n', sys)
        p = Package('name', 'ver', 'rel', 'ep', 'arch', vendor, 'n', sys)
        self.assertEqual(p.nofiles, '2')

    def test_init_package_status_voted(self):
        vendor = Vendor('v')
        sys = System('sysid', 'Foo', '0.0', 'i586')
        Package('name', 'ver', 'rel', 'ep', 'arch', vendor, 'v', sys)
        p = Package('name', 'ver', 'rel', 'ep', 'arch', vendor, 'v', sys)
        self.assertEqual(p.voted, '2')

    def tearDown(self):
        rdb.flushdb()
