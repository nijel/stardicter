# -*- coding: utf-8 -*-
#
# Copyright © 2006 - 2017 Michal Čihař <michal@cihar.com>
#
# This file is part of Stardicter <https://cihar.com/software/slovnik/>
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
"""Convertor for Slovník cizích slov"""

from stardicter.base import StardictWriter
from stardicter.word import Word

URL = 'http://slovnik-cizich-slov.abz.cz/export.php'


class CzechWriter(StardictWriter):
    url = 'http://slovnik-cizich-slov.abz.cz/'
    name = 'Slovník cizích slov'
    source = 'czech'
    target = 'cizi'
    license = 'CC-BY-3.0'
    bidirectional = False
    download_url = URL
    download_charset = 'iso-8859-2'

    def parse_line(self, line):
        word, pronunciation, explanation = line.split('|')
        return [Word(word, explanation, pronunciation=pronunciation)]

    def get_source_name(self):
        """Name for source file."""
        return 'czech.txt'
