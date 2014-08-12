# -*- coding: utf-8 -*-
#
# Copyright © 2006 - 2014 Michal Čihař <michal@cihar.com>
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

from stardicter.base import StardictWriter
from stardicter.word import Word
import urllib

URL = 'http://slovnik-cizich-slov.abz.cz/export.php'


class CzechWriter(StardictWriter):
    url = 'http://slovnik-cizich-slov.abz.cz/'
    name = u'Slovník cizích slov'
    source = 'czech'
    target = 'cizi'
    license = 'CC-BY-3.0'
    bidirectional = False

    def parse_line(self, line):
        word, pronunciation, explanation = line.split('|')
        return [Word(word, explanation, pronunciation=pronunciation)]

    def download(self):
        '''
        Downloads dictionary data.
        '''
        handle = urllib.urlopen(URL)
        return handle.read().decode('iso-8859-2')
