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

from __future__ import unicode_literals
from stardicter.base import StardictWriter
import urllib
import gzip
try:
    from io import BytesIO
except ImportError:
    from cStringIO import StringIO as BytesIO

URL = 'http://slovnik.zcu.cz/files/slovnik_data_utf8.txt.gz'


class CzechEnglishWriter(StardictWriter):
    url = 'http://slovnik.zcu.cz/'
    name = 'GNU/FDL Anglicko-Český slovník'
    source = 'english'
    target = 'czech'
    license = 'GFDL-1.1'

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
        stringio = BytesIO(handle.read())
        gzhandle = gzip.GzipFile(fileobj=stringio)
        return gzhandle.read().decode('utf-8')

    def get_name(self, forward=True):
        if forward:
            return 'GNU/FDL Anglicko-Český slovník'
        else:
            return 'GNU/FDL Česko-Anglický slovník'
