# -*- coding: utf-8 -*-
#
# Copyright © 2006 - 2016 Michal Čihař <michal@cihar.com>
#
# This file is part of Stardicter <http://cihar.com/software/slovnik/>
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
"""
Main executer for stardict convertor
"""

from __future__ import unicode_literals
from __future__ import print_function
from argparse import ArgumentParser
import sys
import stardicter


def main():
    parser = ArgumentParser(
        description='Generates StarDict compatible dictionaries',
    )
    parser.add_argument(
        'dictionary',
        metavar='DICTIONARY',
        type=str,
        nargs='?',
        help='dictionary to download'
    )
    parser.add_argument(
        '-c',
        '--change',
        action='store_true',
        dest='change',
        default=False,
        help='Generate only on source data change.'
    )
    parser.add_argument(
        '-A',
        '--all',
        action='store_true',
        dest='all',
        default=False,
        help='Generate fomat combinations.'
    )
    parser.add_argument(
        '-a',
        '--ascii',
        action='store_true',
        dest='ascii',
        default=False,
        help='Generate plain ascii dictionary.'
    )
    parser.add_argument(
        '-n',
        '--notags',
        action='store_true',
        dest='notags',
        default=False,
        help='Generate dictionary without pango markup.'
    )
    parser.add_argument(
        '-l',
        '--list',
        action='store_true',
        dest='list',
        default=False,
        help='Lists available dictionaries.'
    )
    parser.add_argument(
        '-d',
        '--directory',
        dest='directory',
        default='.',
        help='Directory where to store generated dictionaries'
    )
    parser.add_argument(
        '-s',
        '--source',
        dest='source',
        default='',
        help='Source language for multilanguage dictionaries'
    )
    parser.add_argument(
        '-t',
        '--target',
        dest='target',
        default='',
        help='Target language for multilanguage dictionaries'
    )
    parser.add_argument(
        '-m',
        '--monthly',
        action='store_true',
        dest='monthly',
        default=False,
        help='Flag indicating montly runs (for checksum checking)'
    )

    options = parser.parse_args()

    if options.list:
        for name in stardicter.DICTIONARIES:
            obj = stardicter.DICTIONARIES[name]
            print(
                '{0}: {1} <{2}>'.format(
                    name, obj.name, obj.url
                )
            )
        return

    if options.dictionary is None:
        print('You have to specify dictionary to process!')
        parser.print_usage()
        sys.exit(1)

    if options.dictionary not in stardicter.DICTIONARIES:
        print('Unknown dictionary, use -l to list available ones.')
        parser.print_usage()
        sys.exit(1)

    keyprefix = ''
    if options.monthly:
        keyprefix = 'monthly-'

    writer = stardicter.DICTIONARIES[options.dictionary](
        keyprefix=keyprefix,
        source=options.source,
        target=options.target
    )

    # Change detection
    if options.change and not writer.was_changed():
        sys.exit(0)

    # Load data
    writer.parse()

    # Write dictionaries
    if options.all:
        params = (
            (True, True),
            (True, False),
            (False, True),
            (False, False),
        )
    else:
        params = ((options.ascii, options.notags),)

    for param in params:
        writer.ascii = param[0]
        writer.notags = param[1]
        writer.write_dict(options.directory)

    # Change detection
    if options.change:
        writer.save_checksum()
