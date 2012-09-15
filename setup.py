#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2012 by Tomasz Wójcik <tomek@bthlabs.pl>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import codecs
from setuptools import setup

version = '0.1.2'

desc_file = codecs.open('README.rst', 'r', 'utf-8')
long_description = desc_file.read()
desc_file.close()

setup(
    name="Flask-HTAuth",
    version=version,
    packages=['flask_htauth'],
    test_suite='nose.collector',
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask>=0.6',
    ],
    tests_require=[
        'nose',
    ],
    author=u'Tomasz Wójcik'.encode('utf-8'),
    author_email='tomek@bthlabs.pl',
    maintainer=u'Tomasz Wójcik'.encode('utf-8'),
    maintainer_email='tomek@bthlabs.pl',
    url='http://tomekwojcik.github.com/flask-htauth/',
    download_url='https://github.com/tomekwojcik/flask-htauth/tarball/v%s' % version,
    description='Easy to integrate basic HTTP authentication for Flask apps',
    long_description=long_description,
    license='https://github.com/tomekwojcik/flask-htauth/blob/master/LICENSE',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)