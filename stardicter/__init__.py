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

import codecs

from stardicter.czech import CzechWriter
from stardicter.czechgerman import CzechGermanWriter
from stardicter.czechenglish import CzechEnglishWriter
from stardicter.dictsinfo import DictsInfoWriter
from stardicter.deaccent import deaccent

# List of known dictionaries writers
DICTIONARIES = {
    'czech': CzechWriter,
    'czechgerman': CzechGermanWriter,
    'czechenglish': CzechEnglishWriter,
    'dictsinfo': DictsInfoWriter,
}

# Register deaccenting codec
codecs.register_error('deaccent', deaccent)

__version__ = '0.10'
