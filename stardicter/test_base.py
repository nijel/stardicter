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

import unittest
import tempfile
import os.path
import shutil
from base import StardictWriter


class BaseTest(unittest.TestCase):
    '''
    Testing of base object.
    '''
    def test_checksum(self):
        '''
        Test checksum generating.
        '''
        writer = StardictWriter()
        self.assertEqual(writer.checksum, '4e99e8c12de7e01535248d2bac85e732')

    def test_write(self):
        '''
        Test dictionary writing.
        '''
        directory = tempfile.mkdtemp()
        writer = StardictWriter()
        writer.write_dict(directory)
        self.assertTrue(os.path.exists(os.path.join(directory, 'README')))
        self.assertTrue(os.path.exists(os.path.join(directory, 'aa-bb.dict')))
        self.assertTrue(os.path.exists(os.path.join(directory, 'bb-aa.ifo')))
        self.assertTrue(os.path.exists(os.path.join(directory, 'bb-aa.idx')))
        shutil.rmtree(directory)
