Stardicter
==========

Conversion tools from various formats to StarDict_.


You can find more information at project website:

http://cihar.com/software/slovnik/

Git repository is available at GitHub: 

https://github.com/nijel/stardicter

Requirements
============

Scripts require dictzip to compress dictionaries. You can get it from 
http://sourceforge.net/projects/dict/

Installation
============

You can either clone the git repositry and run the scripts from it or install
using pip::

    pip install stardicter

Usage
=====

The main script is ``sdgen.py``, it downloads and generates StarDict
dictionaries. Check it's help for more information.

Additionally there are some helper script which directly generate tarballs with
dictionary.

Generating dictionary from dicts.info
=====================================

The http://dicts.info/ server provides downloadable dictionaries for many
languages. Unfortunately the license does not allow redistribution, so you need
to generate them yourself. With stardicter it is easy:

    ./dicts_info_tarball.sh italian czech

This generates tarball with italian-czech dictionary. You can choose any
language provided by the service.

Build status
============

.. image:: https://travis-ci.org/nijel/stardicter.svg?branch=master
    :target: https://travis-ci.org/nijel/stardicter
    :alt: Build Status

.. image:: https://landscape.io/github/nijel/stardicter/master/landscape.svg?style=flat
    :target: https://landscape.io/github/nijel/stardicter/master
    :alt: Code Health

.. image:: http://codecov.io/github/nijel/stardicter/coverage.svg?branch=master
    :target: http://codecov.io/github/nijel/stardicter?branch=master
    :alt: Code coverage

.. image:: https://img.shields.io/pypi/dm/stardicter.svg
    :target: https://pypi.python.org/pypi/stardicter
    :alt: PyPI package


License
=======

Copyright (c) 2006 - 2016 Michal Čihař

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see http://www.gnu.org/licenses/.

.. _StarDict: http://stardict.sourceforge.net/
