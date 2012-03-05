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

from flask import abort, render_template, request
from sqlalchemy.orm.exc import NoResultFound

from popcorn import app
from popcorn.models import Distro, System, Vendor
from popcorn.parse import FormatError, EarlySubmissionError, parse_text

@app.route('/', methods=['GET'])
def index():
    distros = Distro.query.all()
    vendors = Vendor.query.all()
    return render_template('index.html', distros=distros, vendors=vendors)

@app.route('/', methods=['POST'])
def receive_submission():
    f = request.files['popcorn']
    try:
        parse_text(f.read())
    except (EarlySubmissionError, FormatError), e:
        return str(e)
    return 'Submission received. Thanks!'
    
@app.route('/vendor/<vendor_name>')
def vendor(vendor_name):
    """Return a Vendor object

    :vendor_name: the name of the Vendor

    """
    try:
        vendor = Vendor.query.filter_by(vendor_name=vendor_name).one()
    except NoResultFound:
        abort(404)
    return render_template('vendor.html', vendor=vendor)

@app.route('/submission/<sub_id>')
def submission(sub_id):
    """Return a Submission object"""
    try:
        sub = Submission.find(sub_id)
    except NoResultFound:
        abort(404)
    return render_template('submission.html', submission=sub)

@app.route('/system/<hwuuid>')
def system(hwuuid):
    """Return a System object"""
    try:
        system = System.query.filter_by(sys_hwuuid=hwuuid).one()
    except NoResultFound:
        abort(404)
    return render_template('system.html', system=system)

@app.route('/package/<pkg_id>')
def package(pkg_id):
    """Return a Package object"""
    try:
        pkg = Package.find(pkg_id)
    except NoResultFound:
        abort(404)
    return render_template('package.html', package=pkg)

@app.route('/distro/<name>_<version>')
def distro(name, version):
    """Return a Distro object"""
    try:
        distro = Distro.query.filter_by(distro_name=name,
                                        distro_version=version).one()
    except NoResultFound:
        abort(404)
    return render_template('distro.html', distro=distro)
