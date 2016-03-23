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
Various helper utilities for stardicter.
"""


def xmlescape(text):
    '''
    Escapes special xml entities.
    '''
    return text.replace(
        '&', '&amp;'
    ).replace(
        '<', '&lt;'
    ).replace(
        '>', '&gt;'
    )


def reformat(text):
    '''
    Cleanup usual junk found in words from database.
    '''
    return text.replace(
        '\\"', '"'
    ).replace(
        '\\\'', '\''
    ).replace(
        '\n', ' '
    ).replace(
        '\r', ' '
    ).strip()
