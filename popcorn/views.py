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

import json
import gzip

from flask import abort, render_template, request, redirect, url_for
from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound

from popcorn import app
from popcorn.database import db_session
from popcorn.parse import FormatError, EarlySubmissionError, parse_text
from popcorn.models import (Distro, SubmissionPackage, Submission,
                            System, Vendor)
from popcorn.pagination import Pagination
from popcorn.helpers import render

PER_PAGE = 50


@app.route('/', methods=['GET'])
@render(template='index.html')
def index():
    distros = Distro.query.all()
    vendors = Vendor.query.all()

    # packages by distro
    # XXX think about moving this to the model
    distro_packages = db_session.query(
        Distro.distro_name, func.count(SubmissionPackage.pkg_name)
    ).select_from(
        SubmissionPackage
    ).join(
        System
    ).join(
        Distro
    ).group_by(Distro.distro_name).all()

    # transform the list of tuples returned by SQLA into a nested JS array
    distro_packages = json.dumps(distro_packages)
    return dict(distros=[i.serialize for i in distros], vendors=[i.serialize
                for i in vendors], distro_packages=distro_packages)


@app.route('/', methods=['POST'])
def receive_submission():
    f = request.files['popcorn']
    if request.headers.get('Content-Encoding') == 'gzip':
        with gzip.GzipFile(fileobj=f, mode='rb') as g:
            try:
                submission = g.read()
            except IOError:
                submission = f.read()
    else:
        submission = f.read()
    try:
        parse_text(submission)
    except (EarlySubmissionError, FormatError), e:
        return str(e)
    return 'Submission received. Thanks!'


@app.route('/vendor/<vendor_name>')
@render(template='vendor.html')
def vendor(vendor_name):
    """Return a Vendor object

    :vendor_name: the name of the Vendor

    """
    try:
        vendor = Vendor.query.filter_by(vendor_name=vendor_name).one()
    except NoResultFound:
        abort(404)
    return dict(vendor=vendor.serialize)


@app.route('/system/<hwuuid>/submission/<sub_date>/')
def submission(hwuuid, sub_date):
    """Return a Submission object"""
    try:
        sub = Submission.query.filter_by(
            sys_hwuuid=hwuuid, sub_date=sub_date).one()
    except NoResultFound:
        abort(404)
    page = request.args.get('page', 0, type=int)
    packages = sub.submission_packages
    count = len(packages)
    pagination = Pagination(page, PER_PAGE, count)
    if page:
        packages = packages[pagination.start:pagination.end + 1]
        if page > pagination.pages:
            abort(404)
    return render_template('submission.html', submission=sub,
                           pagination=pagination, packages=packages)


@app.route('/system/<hwuuid>')
@render(template='system.html')
def system(hwuuid):
    """Return a System object"""
    try:
        system = System.query.filter_by(sys_hwuuid=hwuuid).one()
    except NoResultFound:
        abort(404)
    return dict(system=system.serialize)


# TODO this could be breadcrumbs, where you can put in as many arguments
# as you want and get as much information back, i.e. put in name,
# release and version and get all the arches, epochs, statuses with
# links
@app.route('/package/<name>/<version>/<release>/<arch>')
@app.route('/package/<name>/<version>/<release>/<epoch>/<arch>')
@render(template='packages.html')
def package(name, version, release, arch, epoch=''):
    """Return a Package object"""

    pkgs = SubmissionPackage.query.filter_by(
        pkg_name=name, pkg_version=version, pkg_release=release,
        pkg_epoch=epoch, pkg_arch=arch).all()
    if not pkgs:
        abort(404)

    pkg_statuses = db_session.query(
        SubmissionPackage.pkg_status,
        func.count(SubmissionPackage.pkg_status)
    ).filter_by(
        pkg_name=name, pkg_version=version, pkg_release=release,
        pkg_epoch=epoch, pkg_arch=arch
    ).group_by(
        SubmissionPackage.pkg_status).all()
    statuses = dict()
    for k, v in pkg_statuses:
        statuses[k] = v
    print statuses

    return dict(generic_package=pkgs[0].serialize,
                packages=[i.serialize for i in pkgs], **statuses)


@app.route('/distro/<name>_<version>')
@render(template='distro.html')
def distro(name, version):
    """Return a Distro object"""
    try:
        distro = Distro.query.filter_by(distro_name=name,
                                        distro_version=version).one()
    except NoResultFound:
        abort(404)
    return dict(distro=distro.serialize)
