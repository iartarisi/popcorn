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

from datetime import date

import redis

import tornado.ioloop
import tornado.web

rdb = redis.Redis(host='localhost', port=6379, db=0)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        """Front page"""
        hw_uuids = rdb.lrange('hw-uuids', 0, -1)

        total_packages = rdb.get('global:nextPackageId')

        names, voted, recent, old, nofiles = get_sorted_packages()
        vendors = rdb.smembers('vendors')
        vendor_keys = ['vendor:%s' % i for i in vendors]
        vendor_ids = rdb.mget(vendor_keys)
        self.render('index.html',
                    vendors=vendors,
                    vendor_ids=vendor_ids,
                    systems=hw_uuids,
                    total_packages=total_packages,
                    names=names,
                    voted=voted,
                    recent=recent,
                    old=old,
                    nofiles=nofiles)


class SystemHandler(tornado.web.RequestHandler):
    def get(self, hw_uuid):
        """Display information about a system indentified by its 'hw_uuid'"""
        try:
            system_id = rdb['hw-uuid:%s' % hw_uuid]
        except KeyError:
            raise tornado.web.HTTPError(
                404, "Could not find system with hw-uuid %s", hw_uuid)

        arch = rdb.get('system:%s:arch' % system_id)
        self.write("<h2>System: %s - %s</h2>" % (hw_uuid, arch))
        self.write("<p>Submissions: \n</p>")
        subs = rdb.lrange('system:%s:submissions' % system_id, 0, -1)
        for sub in subs:
            self.write("<a href='/submission/%s'>submission %s</a>" % (sub, sub))


class SubmissionHandler(tornado.web.RequestHandler):
    def get(self, sub_id):
        """Display a submission identified by 'sub_id'"""
        package_ids = rdb.lrange('submission:%s:packages' % sub_id, 0, -1)
        name_keys = ['package:%s:name' % i for i in package_ids]
        package_names = rdb.mget(name_keys)
        self.write('<p>Submission packages:</p>')
        self.write('<ul>')
        for name in package_names:
            self.write('<li>%s</li>' % name)
        self.write('</ul>')

    def post(self):
        """Accepts submissions from popcorn clients in plain text"""
        self.set_header("Content-Type", "text/plain")
        try:
            assert self.request.files['popcorn'][0][
                'content_type'] == 'text/plain', tornado.web.HTTPError(415)
        except KeyError:
            raise Exception("nothing uploaded")

        parse_popcorn(self.request.files['popcorn'][0]['body'])

        self.write('Submission received. Thank you!')


class VendorHandler(tornado.web.RequestHandler):
    def get(self, vendor_id):
        """Display information about a specific vendor"""
        vendor_name = rdb['vendor:%s' % vendor_id]
        packages = rdb.smembers('vendor:%s:packages' % vendor_id)
        if not packages:
            raise tornado.web.HTTPError(
                404, 'Could not find vendor identified by %s' % vendor_id)
        self.write('<p>Packages provided by %s:</p>' % vendor_name)
        self.write('<ul>')
        for package in packages:
            self.write('<li>%s</li>' % rdb.get('package:%s:name' % package))
        self.write('</ul>')


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

def get_system_id(hw_uuid):
    """Check if the system is in our database and create it if it isn't

    :arg hw-uuid: smolt hw-uuid to uniquely indentify each system

    Returns the internal system_id of this system.

    """
    key = 'hw-uuid:%s' % hw_uuid
    try:
        system_id = rdb[key]
    except KeyError:
        system_id = str(rdb.incr('global:nextSystemId'))
        rdb.lpush('hw-uuids', hw_uuid)
        rdb[key] = system_id
    return system_id

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

def get_submission(system_id):
    """Get a new submission for this system_id"""
    # create new submission
    sub_id = str(rdb.incr('global:nextSubmissionId'))
    sub_date = date.today().strftime('%y-%m-%d')
    rdb.set('submission:%s:date', sub_date)

    # attach submission to system
    rdb.lpush('system:%s:submissions' % system_id, sub_id)

    return sub_id

def normalize_vendor(vendor_name):
    # redis keys cannot contain spaces
    return vendor_name.replace(' ', '_')

def get_vendor_id(name):
    """Get or create a new vendor"""
    name = normalize_vendor(name)
    try:
        vendor_id = rdb['vendor:%s' % name]
    except KeyError:
        vendor_id = str(rdb.incr('global:nextVendorId'))
        rdb.set('vendor:%s' % name, vendor_id)
        rdb.set('vendor:%s' % vendor_id, name)
        rdb.sadd('vendors', name)
    return vendor_id
    
def parse_popcorn(data):
    datalines = data.splitlines()
    (popcorn, version, arch, hw_uuid) = datalines[0].split()

    system_id = get_system_id(hw_uuid)
    rdb.set('system:%s:arch' % system_id, arch)
    # TODO check if system can submit based on date
    sub = get_submission(system_id)
    rdb.set('submission:%s:popcorn' % sub, version)
    for line in datalines[1:]:
        (status, name, version, release, arch, vendor) = line.split(None, 5)
        vendor_id = get_vendor_id(vendor)
        package_id = get_package_id(name, version, release, arch, vendor_id)
        if status == 'v':
            rdb.incr('package:%s:voted' % package_id)
        elif status == 'r':
            rdb.incr('package:%s:recent' % package_id)
        elif status == 'o':
            rdb.incr('package:%s:old' % package_id)
        elif status == 'n':
            rdb.incr('package:%s:nofiles' % package_id)
        # add package to the submission
        rdb.lpush('submission:%s:packages' % sub, package_id)

application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/system/([a-f0-9\-]+)", SystemHandler),
        (r"/submission/([0-9]+)?", SubmissionHandler),
        (r"/vendor/([0-9]+)", VendorHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
