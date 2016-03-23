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

import stardicter.dictsinfo
from stardicter.test_base import BaseTest


class DictsInfoTest(BaseTest):
    writer_class = stardicter.dictsinfo.DictsInfoWriter

    def get_writer(self):
        '''
        Gets prepared writer class.
        '''
        return self.writer_class(
            source='english',
            target='czech',
        )

    def test_invalid(self):
        '''
        Test for invalid code.
        '''
        writer = self.writer_class(
            source='english',
            target='invalid',
        )
        self.assertRaisesRegexp(
            ValueError,
            'Failed to fetch data, probably due to invalid language name.',
            writer.download
        )

    def test_same(self):
        '''
        Test for same languages.
        '''
        writer = self.writer_class(
            source='english',
            target='english',
        )
        self.assertRaisesRegexp(
            ValueError,
            'You cannot select two same languages.',
            writer.download
        )
