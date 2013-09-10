# -*- coding: utf-8 -*-
#
# Copyright © 2006 - 2013 Michal Čihař <michal@cihar.com>
#
# This file is part of Weblate <http://weblate.org/>
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

import unicodedata


def deaccent(exc):
    '''
    Removes accents on string conversion errors.
    '''
    if not isinstance(exc, UnicodeEncodeError):
        raise TypeError("don't know how to handle %r" % exc)
    result = []
    for current in exc.object[exc.start:exc.end]:
#        print '"%s" %d' % (current, ord(current))
        if current in (u'\x93', u'\x94', u'\x84'):
            result.append('"')
            continue
        elif current == u'\x92':
            result.append('\'')
            continue
        name = unicodedata.name(current)
        if name[:18] == 'LATIN SMALL LETTER':
            result.append(unicode(name[19].lower()))
        elif name[:20] == 'LATIN CAPITAL LETTER':
            result.append(unicode(name[21]))
        elif name == 'ACUTE ACCENT':
            result.append('\'')
        elif name == 'NO-BREAK SPACE':
            result.append(' ')
        elif name == 'MULTIPLICATION SIGN':
            result.append('x')
        elif name == 'DEGREE SIGN':
            result.append('<degree>)')
        elif name == 'SECTION SIGN':
            # §
            result.append('<paragraph>')
        elif name == 'DIVISION SIGN':
            # ÷
            result.append('/')
        else:
            raise ValueError(
                'Can not convert to ASCII: %s (%s)' % (current, name)
            )
    return (u''.join(result), exc.end)
