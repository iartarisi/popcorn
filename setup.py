#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="popcorn",
    version="0.1",
    url="http://github.com/mapleoin/popcorn",
    author="Ionuț Arțăriși",
    author_email="mapleoin@lavabit.com",
    long_description=__doc__,
    packages=find_packages(exclude=["*.test", "test", "*.test.*"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask', 'sqlalchemy', 'psycopg2'],
    test_suite="popcorn.test"
    )
