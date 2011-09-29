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

class Vendor(object):
    """A vendor is the provider of a repository.

    It is identified by a normalized name of the target repository.

    The key 'vendor:%(vendor)s' holds a hash with the keys:
     - name - the name of this repository

    The key 'vendor:%(vendor)s:packages' holds a set of all the package
    ids belonging to this vendor.

    """
    def __init__(self, name):
        """
        Retrieves or creates a Vendor object.

        :name: the name string of this Vendor

        """
        self.name = name
        self.key = _normalize_vendor(name)
        try:
            rdb['vendor:%s' % self.key]
        except KeyError:
            rdb.set('vendor:%s' % self.key, name)
            rdb.sadd('vendors', self.key)

def _normalize_vendor(vendor_name):
    # redis keys cannot contain spaces
    return vendor_name.replace(' ', '_')
