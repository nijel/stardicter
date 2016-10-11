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
from stardicter.utils import reformat, xmlescape

FMT_TYPE = '<span size="larger" color="darkred" weight="bold">{0}</span>\n'
FMT_DETAILS = '<i>{0}</i> '
FMT_TRANSLATE = '<b>{0}</b>'
FMT_NOTE = ' ({0})'
FMT_AUTHOR = ' <small>[{0}]</small>'
FMT_PRONUNCIATION = '[<i>{0}</i>]\n\n'


class Word(object):
    '''
    Class holding single word.
    '''
    def __init__(self, word, translation, wtype='', note='', author='',
                 pronunciation=''):
        self.word = word
        self.translation = translation
        self.wtype = wtype
        self.note = note
        self.author = author
        self.pronunciation = pronunciation

    def reverse(self):
        '''
        Returns copy of a object for reverse direction.
        '''
        return Word(
            self.translation, self.word, self.wtype, self.note, self.author,
            self.pronunciation
        )

    @staticmethod
    def from_slovnik(line):
        '''
        Parses word from format used by https://www.svobodneslovniky.cz/
        '''
        # split it up
        parts = line.split('\t')
        if len(parts) == 5:
            word, translation, wtype, note, author = parts
        elif len(parts) == 6:
            # Extra word
            word, ignore, translation, wtype, note, author = parts
            word += ignore
        elif len(parts) == 1:
            # Missing author, translation, type and note
            word = parts[0]
            translation = ''
            wtype = ''
            author = ''
            note = ''
        elif len(parts) == 2:
            # Missing author, type and note
            word, translation = parts
            wtype = ''
            author = ''
            note = ''
        elif len(parts) == 3:
            # Missing author and note
            word, translation, wtype = parts
            author = ''
            note = ''
        elif len(parts) == 4:
            # Missing author
            word, translation, wtype, note = parts
            author = ''
        else:
            raise ValueError('Invalid input: {0!r}'.format(line))

        return Word(
            word=reformat(word),
            translation=reformat(translation),
            wtype=reformat(wtype),
            note=reformat(note),
            author=reformat(author)
        )

    def format(self):
        '''
        Returns formatted dictionary entry.
        '''
        result = []
        if self.pronunciation != '':
            result.append(
                FMT_PRONUNCIATION.format(xmlescape(self.pronunciation))
            )
        if self.wtype != '':
            result.append(FMT_DETAILS.format(xmlescape(self.wtype)))
        result.append(FMT_TRANSLATE.format(xmlescape(self.translation)))
        if self.note != '':
            result.append(FMT_NOTE.format(xmlescape(self.note)))
        if self.author != '':
            result.append(FMT_AUTHOR.format(xmlescape(self.author)))
        result.append('\n')
        return ''.join(result)
