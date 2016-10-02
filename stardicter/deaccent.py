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

from __future__ import unicode_literals
import unicodedata


SIMPLE_MAPS = {
    'ACUTE ACCENT': '\'',
    'NO-BREAK SPACE': ' ',
    'THIN SPACE': ' ',
    'MULTIPLICATION SIGN': 'x',
    'DEGREE SIGN': '<degree>',
    # §
    'SECTION SIGN': '<paragraph>',
    # ÷
    'DIVISION SIGN': '/',
    # „
    'DOUBLE LOW-9 QUOTATION MARK': '"',
    # “
    'LEFT DOUBLE QUOTATION MARK':  '"',
}


def deaccent(exc):
    '''
    Removes accents on string conversion errors.
    '''
    if not isinstance(exc, UnicodeEncodeError):
        raise TypeError("don't know how to handle {0}".format(exc))
    result = []
    for current in exc.object[exc.start:exc.end]:
        #  print('"{0}" {1}'.format(current, ord(current)))
        if current in ('\x93', '\x94', '\x84'):
            result.append('"')
            continue
        elif current == '\x92':
            result.append('\'')
            continue
        name = unicodedata.name(current)
        if name[:18] == 'LATIN SMALL LETTER':
            result.append(name[19].lower())
        elif name[:20] == 'LATIN CAPITAL LETTER':
            result.append(name[21])
        elif name in SIMPLE_MAPS:
            result.append(SIMPLE_MAPS[name])
        else:
            raise ValueError(
                'Can not convert to ASCII: {0} ({1})'.format(current, name)
            )
    return (''.join(result), exc.end)
