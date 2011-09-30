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
from popcorn.exceptions import FormatError

class Package(object):
    """A package object

    A package is identified by its NVREA and vendor in the normal NVREA
    form and stored under ``vendor:%(vendor)s:package`` like so:
    ``vendor:%(vendor)s:package:%(name)s-%(version)s-%(release)s[:%(epoch)s]?:%(arch)s``.

    Ids are stored in the key above and incremented in
    ``global:nextPackageId``.

    Packages belong to a vendor and their ids are stored in the set
    ``vendor:%(vendor_id)s:packages``.

    A list of package statuses are stored in
    ``package:%(package_id)s:status`` as a hash with these keys:
    'voted', 'recent', 'old' and 'nofiles'. The values are integers. The
    status of a package in one submission on the system that it was sent
    from is stored in 'package:%s:status'.

    """
    def __init__(self, name, version, release, epoch,
                 arch, vendor, status, system):
        """Get or create a package object"""
        self.name = name
        self.version = version
        self.release = release
        self.arch = arch
        self.vendor = vendor
        self.epoch = epoch
        self.status = _get_status(status)
        self.system = system

        sepoch = ":"+epoch if epoch != 'None' else ''
        self.full_name = ("%(name)s-%(version)s-%(release)s%(sepoch)s.%(arch)s"
                          % locals())

        key = ('vendor:%(vendor)s:package:%(full_name)s' % self.__dict__)

        try:
            self.id = rdb[key]
        except KeyError:
            self.id = str(rdb.incr('global:nextPackageId'))
            rdb[key] = self.id
            # status on system
            rdb['system:%s:package:%s:status'] = self.status
            rdb.sadd("vendor:%s:packages" % vendor, self.id)
        rdb.hincrby('package:%s:status' % self.id, self.status, 1)

    def __repr__(self):
        return self.full_name

    def status_on_system(self, system):
        """Return a string with this Package's status on System ``system``"""
        
    @property
    def old(self):
        return rdb.hget('package:%s:status' % self.id, 'old')

    @property
    def recent(self):
        return rdb.hget('package:%s:status' % self.id, 'recent')

    @property
    def nofiles(self):
        return rdb.hget('package:%s:status' % self.id, 'nofiles')

    @property
    def voted(self):
        return rdb.hget('package:%s:status' % self.id, 'voted')

def _get_status(s):
    status_map = {'v': 'voted',
                  'r': 'recent',
                  'o': 'old',
                  'n': 'nofiles'}
    try:
        status = status_map[s]
    except KeyError:
        raise FormatError("the package's status could not be recognized.")
    return status
