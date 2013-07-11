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

from stardicter.base import StardictWriter
from stardicter.word import Word
import urllib2

BASEURL = 'http://www.dicts.info/uddl.php?l1=%s&l2=%s&format=text'


class DictsInfoWriter(StardictWriter):
    url = 'http://www.dicts.info/'
    name = u'dicts.info'
    license = 'non redistributable license'

    def is_header_line(self, line):
        '''
        Checks whether line is header.
        '''
        return line.startswith('#')

    def add_description(self, line):
        '''
        Adds description from line.
        '''
        self.description += line[2:]

    def is_data_line(self, line):
        '''
        Checks whether line is used for checksum. Can be used to exclude
        timestamps from data.
        '''
        return 'created from the Universal dictionary at' not in line

    def parse_line(self, line):
        words, translations, wtype = line.split('\t')
        words = words.split(';')
        translations = translations.split(';')
        for word in words:
            for translation in translations:
                yield Word(word, translation, wtype=wtype)

    def download(self):
        '''
        Downloads dictionary data.
        '''
        handle = urllib2.urlopen(
            BASEURL % (self.source, self.target),
            'ok=selected'
        )
        data = handle.read().decode('utf-8')

        if 'You cannot select two same languages.' in data:
            raise ValueError(data)

        if 'SQL select error' in data:
            raise ValueError(
                'Failed to fetch data, probably due to invalid language name'
            )

        return data
