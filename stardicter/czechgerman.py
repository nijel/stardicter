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

URL = 'http://slovnik.hrach.eu/index.php?id=6&sablona=export&format=zcu'


class CzechGermanWriter(StardictWriter):
    url = 'http://slovnik.hrach.eu/'
    name = u'GNU/FDL Německo-Český slovník'
    source = 'german'
    target = 'czech'
    license = 'GNU/FDL license'

    def is_data_line(self, line):
        '''
        Checks whether this is line with timestamp.
        '''
        return not line.startswith('# File generated')

    def is_header_line(self, line):
        return line[0] == '#'

    def download(self):
        '''
        Downloads dictionary data.
        '''
        handle = urllib.urlopen(URL)
        return handle.read().decode('utf-8')

    def get_name(self, forward=True):
        if forward:
            return u'GNU/FDL Česko-Německý slovník'
        else:
            return u'GNU/FDL Německo-Český slovník'
