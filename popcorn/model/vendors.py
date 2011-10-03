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

import urlparse

from popcorn.configs import rdb
from popcorn.model.error import DoesNotExist
from popcorn.model.utils import list_to_tuples

class Vendor(object):
    """A Vendor is the provider of a repository.

    It is identified by a normalized url of the target repository.  The
    key 'global:nextVendorId' is incremented to generate a new id which
    is stored in 'vendor:%(n_url)s'. All the ids are stored in the set
    'vendors'. The key/n_url can be found in 'vendor:%(vendor_id)s:key'.
    The vendor object's attributes (for now just the original ``url``)
    can be found in the hash at 'vendor:%(vendor_id)s'.
    
    The key 'vendor:%(vendor)s:packages' holds a set of all the package
    ids belonging to this vendor.

    """
    @classmethod
    def get_all_ids(cls):
        """Return a set of all the vendor ids we currently have"""
        return rdb.smembers('vendors')

    @classmethod
    def find(cls, vendor_id):
        """Return the Vendor object with the given ``vendor_id``"""
        try:
            key = rdb['vendor:%s:key' % vendor_id]
        except KeyError:
            raise DoesNotExist('Vendor', vendor_id)
        return Vendor(key, existing=True)

    def __init__(self, url, existing=False):
        """Retrieves or creates a Vendor object

        A new Vendor object is created only if ``existing`` is set to
        False (the default), otherwise a DoesNotExist error is raised
        when trying to initialize a Vendor object with a new url.

        :url: a vanilla url string which identifies the Vendor
        :existing: True if we expect the Vendor object to already exist

        """
        self.key = _normalize_url(url)
        try:
            self.id = rdb['vendor:%s' % self.key]
        except KeyError:
            if existing:
                raise DoesNotExist('Vendor', self.key)
            self.id = str(rdb.incr('global:nextVendorId'))
            rdb.set('vendor:%s' % self.key, self.id)
            rdb.set('vendor:%s:key' % self.id, self.key)
            rdb.hset('vendor:%s' % self.id, 'url', url)
            rdb.sadd('vendors', self.id)
            self.url = url
        else:
            self.url = rdb.hget('vendor:%s' % self.id, 'url')

    def __repr__(self):
        return self.id

    @property
    def package_nvreas(self):
        """Return a list of all the packages of this vendor

        Returns a list of tuples of this form: (package_id,
        package_nvrea) ordered by NVREA.

        """
        ids_and_names = rdb.sort('vendor:%s:packages' % self.id,
                                 by='package:*:nvrea', alpha=True,
                                 get=['#', 'package:*:nvrea'])
        return list_to_tuples(ids_and_names, 2)
        

def _normalize_url(url):
    """Normalize a URL so we can use it as a redis key"""
    r = urlparse.urlsplit(url.replace(' ', ''))
    return r.geturl()
