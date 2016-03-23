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
from stardicter.base import StardictWriter

URL = (
    'http://gnu.nemeckoceskyslovnik.cz/'
    'index.php?id=6&sablona=export&format=zcu'
)


class CzechGermanWriter(StardictWriter):
    url = 'http://www.nemeckoceskyslovnik.cz/'
    name = 'GNU/FDL Německo-Český slovník'
    source = 'german'
    target = 'czech'
    license = 'GFDL-1.1'
    download_url = URL

    def is_data_line(self, line):
        '''
        Checks whether this is line with timestamp.
        '''
        return not line.startswith('# File generated')

    def get_name(self, forward=True):
        if forward:
            return 'GNU/FDL Německo-Český slovník'
        else:
            return 'GNU/FDL Česko-Německý slovník'
