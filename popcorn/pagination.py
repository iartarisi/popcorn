# -*- coding: utf-8 -*-
# Copyright (c) 2012 Akshit Khurana <axitkhurana@gmail.com>
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

from math import ceil


class Pagination(object):
    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        """ Returns total pages """
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        """ Returns true if current page has previous pages """
        return self.page > 1

    @property
    def has_next(self):
        """ Returns true if current page has next pages """
        return self.page < self.pages

    @property
    def start(self):
        """ Returns index of first result of current page """
        return (self.page - 1) * self.per_page

    @property
    def end(self):
        """ Returns index of last result of current page """
        return self.start + self.per_page - 1

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        """ Generates page numbers for navigation """
        last = 0
        for num in xrange(1, self.pages + 1):
            if (num <= left_edge
                    or (num > self.page - left_current - 1
                        and num < self.page + right_current)
                    or (num > self.pages - right_edge)):
                if last + 1 != num:
                    yield None
                yield num
                last = num
