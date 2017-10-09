#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2015 Michal Čihař <michal@cihar.com>
#
# This file is part of Odorik <https://github.com/nijel/stardicter>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""Setup file for easy installation."""
import io
import os
from setuptools import setup

VERSION = __import__('stardicter').__version__
README = os.path.join(os.path.dirname(__file__), 'README.rst')

with io.open(README, encoding='utf-8') as readme:
    LONG_DESCRIPTION = readme.read()

REQUIRES = open('requirements.txt').read().split()

setup(
    name='stardicter',
    version=VERSION,
    author='Michal Čihař',
    author_email='michal@cihar.com',
    description=' Conversion tools from various formats to StarDict.',
    license='GPLv3+',
    keywords='stardict,dictionary',
    url='https://cihar.com/software/slovnik/',
    download_url='https://pypi.python.org/pypi/stardicter',
    bugtrack_url='https://github.com/nijel/stardicter/issues',
    platforms=['any'],
    packages=[
        'stardicter',
    ],
    package_data={'stardicter': ['test_*.txt']},
    package_dir={'stardicter': 'stardicter'},
    long_description=LONG_DESCRIPTION,
    install_requires=REQUIRES,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    entry_points={
        'console_scripts': ['sdgen = stardicter.main:main']
    },
)
