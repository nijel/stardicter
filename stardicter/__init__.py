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
"""Main stardicter module."""

import codecs

from stardicter.czech import CzechWriter
from stardicter.czechenglish import CzechEnglishWriter
from stardicter.czechgerman import CzechGermanWriter
from stardicter.deaccent import deaccent
from stardicter.dictsinfo import DictsInfoWriter

# List of known dictionaries writers
DICTIONARIES = {
    "czech": CzechWriter,
    "czechgerman": CzechGermanWriter,
    "czechenglish": CzechEnglishWriter,
    "dictsinfo": DictsInfoWriter,
}

# Register deaccenting codec
codecs.register_error("deaccent", deaccent)
