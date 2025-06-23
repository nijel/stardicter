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
"""Test for dicts.info."""

import pytest

import stardicter.dictsinfo
from stardicter.test_base import BaseTest


class DictsInfoTest(BaseTest):
    writer_class = stardicter.dictsinfo.DictsInfoWriter

    def get_writer(self):
        """Gets prepared writer class."""
        self.skip_net()
        return self.writer_class(
            source="english",
            target="czech",
        )

    @pytest.mark.xfail(reason="server is flaky")
    def test_invalid(self) -> None:
        """Test for invalid code."""
        self.skip_net()
        writer = self.writer_class(
            source="english",
            target="invalid",
        )
        self.assertRaisesRegex(
            ValueError,
            "Failed to fetch data, probably due to invalid language name.",
            writer.download,
        )

    def test_same(self) -> None:
        """Test for same languages."""
        self.skip_net()
        writer = self.writer_class(
            source="english",
            target="english",
        )
        self.assertRaisesRegex(
            ValueError, "You cannot select two same languages.", writer.download
        )
