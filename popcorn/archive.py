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

"""Archive packages from SubmissionPackages model to PackageArchive
model
"""
from datetime import date

from sqlalchemy import func
from sqlalchemy.sql.expression import extract

from popcorn.database import db_session
from popcorn.models import (SubmissionPackage as SubPac, Submission as Sub,
                            PackageArchive)

TODAY = date.today()
LAST_MONTH = TODAY.replace(month=TODAY.month - 1)


def update_archives(arc_month=LAST_MONTH):
    """Archives packages of a month, by default: last month"""
    query = db_session.query(SubPac.pkg_name, SubPac.pkg_version,
                             SubPac.pkg_release, SubPac.pkg_arch,
                             SubPac.vendor_name, SubPac.pkg_status,
                             Sub.distro_name, Sub.distro_version,
                             func.min(SubPac.sub_date),
                             func.count('*').label('count')
                             ).join(Sub)

    arcs = query.filter(extract('month', SubPac.sub_date) == arc_month.month,
                        extract('year', SubPac.sub_date) == arc_month.year
                        ).group_by(extract('month', SubPac.sub_date),
                                   extract('year', SubPac.sub_date),
                                   SubPac.pkg_name, SubPac.pkg_version,
                                   SubPac.pkg_release, SubPac.pkg_arch,
                                   SubPac.vendor_name,
                                   SubPac.pkg_status, Sub.distro_name,
                                   Sub.distro_version).all()

    pkg_archives = []
    for pkg in arcs:
        pkg_archives.append(PackageArchive(*pkg))

    for pkg_archive in pkg_archives:
        pkg_archive.month = pkg_archive.month.replace(day=1)

    db_session.add_all(pkg_archives)
    db_session.commit()

if __name__ == '__main__':
    update_archives()
