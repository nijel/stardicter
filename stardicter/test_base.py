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
import stardicter.base


class BaseTest(unittest.TestCase):
    writer_class = stardicter.base.StardictWriter

    def test_write(self):
        '''
        Test dictionary writing.
        '''
        writer = self.writer_class()
        directory = tempfile.mkdtemp()
        writer.write_dict(directory)
        self.assertTrue(os.path.exists(os.path.join(directory, 'README')))
        shutil.rmtree(directory)


class CoreTest(unittest.TestCase):
    '''
    Testing of base object.
    '''
    def test_checksum(self):
        '''
        Test checksum generating.
        '''
        writer = stardicter.base.StardictWriter()
        self.assertEqual(writer.checksum, '4e99e8c12de7e01535248d2bac85e732')

    def changes_testing(self, name):
        '''
        Core for changes testing.
        '''
        backup = stardicter.base.CONFIGFILE
        stardicter.base.CONFIGFILE = name
        writer = stardicter.base.StardictWriter()
        self.assertTrue(writer.was_changed())
        writer.save_checksum()
        self.assertFalse(writer.was_changed())
        stardicter.base.CONFIGFILE = backup

    def test_changes(self):
        '''
        Test changes detection with empty config file.
        '''
        with tempfile.NamedTemporaryFile(delete=True) as temp:
            self.changes_testing(temp.name)

    def test_changes_nofile(self):
        '''
        Test changes detection without config file.
        '''
        temp = tempfile.NamedTemporaryFile(delete=True)
        temp.close()
        self.changes_testing(temp.name)
