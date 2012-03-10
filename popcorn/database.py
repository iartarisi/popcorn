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

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from popcorn.configs import DB_ENGINE


engine = create_engine(DB_ENGINE, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# import all modules here that might define models so that
# they will be registered properly on the metadata.
import popcorn.models

def init_db():
    Arch, Status = popcorn.models.Arch, popcorn.models.PackageStatus

    Base.metadata.create_all(bind=engine)
    # TODO think about having only one arch for i?86
    db_session.add_all([Arch('noarch'), Arch('i586'), Arch('i686'),
                        Arch('i486'), Arch('i386'), Arch('x86_64'),
                        Arch('ppc'), Arch('ppc64'), Arch('s390'),
                        Status('voted'), Status('nofiles'),
                        Status('recent'), Status('old')])
    db_session.commit()

def drop_db():
    Base.metadata.drop_all(bind=engine)
