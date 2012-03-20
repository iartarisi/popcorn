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
            if (num <= left_edge or
                (num > self.page - left_current - 1 and
                num < self.page + right_current) or
                num > self.pages - right_edge):
                if last + 1 != num:
                    yield None
                yield num
                last = num
