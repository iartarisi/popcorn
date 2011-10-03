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

import sys

from flask import Flask, abort, render_template, request
app = Flask("popcorn")

from popcorn.configs import rdb
from popcorn.model import System, Vendor
from popcorn.model.error import DoesNotExist

from popcorn.parse import parse_text

sys.path.append("/home/mapleoin/popcorn/")

@app.route('/', methods=['GET'])
def index():
    systems = System.get_all_ids()
    vendors = Vendor.get_all_ids()
    return render_template('index.html',
                           systems = systems,
                           vendors = vendors)

@app.route('/', methods=['POST'])
def receive_submission():
    f = request.files['popcorn']
    # TODO exception handling
    parse_text(f.read())
    return 'Submission received. Thanks!'
    
@app.route('/vendor/<vendor_id>')
def vendor(vendor_id):
    """Return a Vendor object

    :vendor_id: the id of the Vendor

    """
    try:
        vendor = Vendor.find(vendor_id)
    except DoesNotExist:
        abort(404)
    return render_template('vendor.html', vendor=vendor)

@app.route('/system/<hw_uuid>')
def system(hw_uuid):
    """Return a System object"""
    try:
        system = System(hw_uuid)
    except DoesNotExist:
        abort(404)
    return render_template('system.html', system=system)

def get_sorted_packages(key='voted'):
    """Get a lists of package attributes sorted by `key`

    The list returned is made of [names, voted, recent, old, nofiles]

    """
    if key not in ['name', 'voted', 'recent', 'old', 'nofiles']:
        raise Exception("Unrecognized key")

    packages_tuples = []
    for attr in ['name', 'voted', 'recent', 'old', 'nofiles']:
        packages_tuples.append(rdb.sort('packageIds',
                                        by='package:*:%s' % key,
                                        desc=True,
                                        get='package:*:%s' % attr))
    return packages_tuples


def get_package_id(name, ver, rel, arch, vendor):
    """Get or create a package for this name, ver, rel, arch, vendor combo"""
    key = 'packageId:%(name)s:%(ver)s:%(rel)s:%(arch)s:%(vendor)s' % locals()
    try:
        package_id = rdb[key]
    except KeyError:
        package_id = str(rdb.incr('global:nextPackageId'))
        rdb[key] = package_id
        rdb.lpush('packageIds', package_id)
        rdb.set('package:%s:name' % package_id, name)
        rdb.sadd('vendor:%s:packages' % vendor, package_id)
    return package_id

if __name__ == "__main__":
    app.debug = True
    app.run()
