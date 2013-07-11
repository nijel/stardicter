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
import urllib
import gzip
import cStringIO

URL = 'http://slovnik.zcu.cz/files/slovnik_data_utf8.txt.gz'


class CzechEnglishWriter(StardictWriter):
    url = 'http://slovnik.zcu.cz/'
    name = u'GNU/FDL Česko-Anglický slovník'
    source = 'czech'
    target = 'english'
    license = 'GNU/FDL license'

    def is_data_line(self, line):
        '''
        Checks whether this is line with timestamp.
        '''
        return not line.startswith('#      Date:')

    def is_header_line(self, line):
        return line[0] == '#'

    def download(self):
        '''
        Downloads dictionary data.
        '''
        handle = urllib.urlopen(URL)
        stringio = cStringIO.StringIO(handle.read())
        gzhandle = gzip.GzipFile(fileobj=stringio)
        return gzhandle.read().decode('utf-8')
