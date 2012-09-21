# -*- coding: utf-8 -*-
# Copyright (c) 2012 Ionuț Arțăriși <iartarisi@suse.cz>
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
import unittest

import flask

from popcorn.helpers import render

class TestHelpers(unittest.TestCase):

    def test_render_html(self):
        app = flask.Flask(__name__)

        @app.route('/')
        @render(template='test.html')
        def index():
            return dict(test_data='foo')

        c = app.test_client()
        response = c.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, '<p>foo')

    def test_render_html_arbitrary_error_code(self):
        app = flask.Flask(__name__)

        @app.route('/')
        @render(template='test.html')
        def index():
            return dict(test_data='foo', status_code=418)

        c = app.test_client()
        response = c.get('/')

        self.assertEqual(response.status_code, 418)
        self.assertEqual(response.data, '<p>foo')

    def test_render_json(self):
        app = flask.Flask(__name__)

        @app.route('/')
        @render(template='test.html')
        def index():
            return dict(test_data='foo')

        c = app.test_client()
        response = c.get('/', headers=[('Accept', 'application/json')])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data),
                         {'test_data': 'foo'})
        self.assertEqual(response.headers['Content-Type'], 'application/json')

    def test_render_json_arbitrary_error_code(self):
        app = flask.Flask(__name__)

        @app.route('/')
        @render(template='test.html')
        def index():
            return dict(test_data='foo', status_code=418)

        c = app.test_client()
        response = c.get('/', headers=[('Accept', 'application/json')])

        self.assertEqual(response.status_code, 418)
        self.assertEqual(json.loads(response.data),
                         {'test_data': 'foo'})
        self.assertEqual(response.headers['Content-Type'], 'application/json')        
