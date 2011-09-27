#!/usr/bin/env python
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

from popcorn.configs import rdb

class Package(object):
    """A package object

    A package is identified by its NVREA in under 'packageId:' like so:
    packageId:%(name)s:%(version)s:%(release)s:%(epoch)s:%(arch)s:%(vendor)s'
    
    Ids are stored in the key above and incremented in
    'global:nextPackageId'.

    Packages belong to a vendor and their ids are stored in the set
    'vendor:%(vendor_id)s:packages'

    """
    def __init__(self, name, version, release, arch, vendor, epoch=None):
        """Get or create a package object"""
        self.name = name
        self.version = version
        self.release = release
        self.arch = arch
        self.vendor = vendor
        self.epoch = epoch

        key = ('packageId:%(name)s:%(version)s:%(release)s:%(epoch)s:'
               '%(arch)s:%(vendor)s' % locals())
        try:
            self.id = rdb[key]
        except KeyError:
            self.id = str(rdb.incr('global:nextPackageId'))
            rdb[key] = self.id
            rdb.sadd("vendor:%s:packages" % vendor, self.id)
