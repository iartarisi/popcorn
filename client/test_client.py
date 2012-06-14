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

from ctypes import c_char_p, CDLL
import BaseHTTPServer
import cgi
import unittest
import threading

DOMAIN = "http://localhost"
PORT = 8000
SUBMISSION_FILE = "/tmp/popcorn.txt"
with open(SUBMISSION_FILE) as f:
    SUBMISSION_TEXT = f.read()

libpopcorn = CDLL('libpopcorn.so')

class TestPostTest(unittest.TestCase):

    def test_server_post(self):
        # we're using a single element list until we get py3.x's nonlocal
        form_value = []
        class TestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
            def do_POST(self):
                form = cgi.FieldStorage(
                    fp=self.rfile, headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'})
                form_value.append(form['popcorn'].value)

        # start an HTTPServer in a different thread which reads the request body
        httpd = BaseHTTPServer.HTTPServer(("", PORT), TestHandler)
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.start()

        libpopcorn.popcornPostData(c_char_p("%s:%s" % (DOMAIN, PORT)),
                                   c_char_p(SUBMISSION_FILE))

        self.assertEqual(form_value[0], SUBMISSION_TEXT)

        httpd.shutdown()
        server_thread.join()
