# -*- coding: utf-8 -*-
#
# Copyright © 2006 - 2014 Michal Čihař <michal@cihar.com>
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

from stardicter.utils import reformat, xmlescape

FMT_TYPE = u'<span size="larger" color="darkred" weight="bold">%s</span>\n'
FMT_DETAILS = u'<i>%s</i> '
FMT_TRANSLATE = u'<b>%s</b>'
FMT_NOTE = u' (%s)'
FMT_AUTHOR = u' <small>[%s]</small>'
FMT_PRONUNCIATION = '[<i>%s</i>]\n\n'


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
        Parses word from format used by http://slovnik.zcu.cz/
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
            raise ValueError('Invalid input: %s' % repr(line))

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
        result = ''
        if self.pronunciation != '':
            result += FMT_PRONUNCIATION % xmlescape(self.pronunciation)
        if self.wtype != '':
            result += FMT_DETAILS % xmlescape(self.wtype)
        result += FMT_TRANSLATE % xmlescape(self.translation)
        if self.note != '':
            result += FMT_NOTE % xmlescape(self.note)
        if self.author != '':
            result += FMT_AUTHOR % xmlescape(self.author)
        result += '\n'
        return result
