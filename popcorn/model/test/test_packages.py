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
from popcorn.model.error import DoesNotExist


class TestPackages(unittest.TestCase):

    def setUp(self):
        self.distro = Distro('Foo', '0.0')
        self.sys = System('sysid', 'Foo', '0.0', 'i586')
        self.vendor = Vendor('v')
        self.sub = Submission(self.sys, 'popver')

    def tearDown(self):
        rdb.flushdb()

    def test_init_package_attributes(self):
        p = Package('name', 'ver', 'rel', 'ep', 'arch',
                    self.vendor, 'o', self.sub)
        self.assertTupleEqual(
            (p.name, p.version, p.release, p.epoch, p.arch,
             p.vendor, p.status, p.sub.__class__),
            ('name', 'ver', 'rel', 'ep', 'arch',
             self.vendor, 'old', Submission))

    def test_init_package_status_old(self):
        Package('name', 'ver', 'rel', 'ep', 'arch', self.vendor, 'o', self.sub)
        p = Package('name', 'ver', 'rel', 'ep', 'arch',
                    self.vendor, 'o', self.sub)
        self.assertEqual(p.old, '2')

    def test_init_package_status_recent(self):
        Package('name', 'ver', 'rel', 'ep', 'arch', self.vendor, 'r', self.sub)
        p = Package('name', 'ver', 'rel', 'ep', 'arch',
                    self.vendor, 'r', self.sub)
        self.assertEqual(p.recent, '2')

    def test_init_package_status_nofiles(self):
        Package('name', 'ver', 'rel', 'ep', 'arch', self.vendor, 'n', self.sub)
        p = Package('name', 'ver', 'rel', 'ep', 'arch',
                    self.vendor, 'n', self.sub)
        self.assertEqual(p.nofiles, '2')

    def test_init_package_status_voted(self):
        Package('name', 'ver', 'rel', 'ep', 'arch', self.vendor, 'v', self.sub)
        p = Package('name', 'ver', 'rel', 'ep', 'arch',
                    self.vendor, 'v', self.sub)
        self.assertEqual(p.voted, '2')

    def test_init_package_already_exists_same_id(self):
        p = Package('name', 'ver', 'rel', 'ep', 'arch',
                    self.vendor, 'v', self.sub)
        sub2 = Submission(self.sys, 'popver')
        r = Package('name', 'ver', 'rel', 'ep', 'arch',
                    self.vendor, 'v', sub2)
        self.assertEqual(p.id, r.id)
        self.assertEqual(len(self.sub.packages), 1)
        self.assertEqual(self.sub.packages.pop().id, '1')

    def test_find_package(self):
        package = Package('name', 'ver', 'rel', 'ep', 'arch',
                          self.vendor, 'v', self.sub)
        self.assertIsInstance(Package.find(1), Package)

    def test_find_package_not_found(self):
        self.assertRaises(DoesNotExist, Package.find, 1)

    def test_status_on_system(self):
        s1 = Submission(self.sys, 'popver')
        Package('name', 'ver', 'rel', 'ep', 'arch', self.vendor, 'v', s1)
        s2 = Submission(self.sys, 'popver')
        Package('name', 'ver', 'rel', 'ep', 'arch', self.vendor, 'r', s2)
        p = Package('name', 'ver', 'rel', 'ep', 'arch', self.vendor, 'o', s2)
        self.assertEqual(p.status_on_system(self.sys), 'old')

    def test_repr(self):
        p = Package('name', 'ver', 'rel', 'ep', 'arch',
                    self.vendor, 'v', self.sub)
        self.assertEqual("%s" % p, "name-ver-rel:ep.arch")
