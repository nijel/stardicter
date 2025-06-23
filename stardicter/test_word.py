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
"""Test for word handling."""

import unittest

from stardicter.word import Word


class WordTest(unittest.TestCase):
    """Word class testsing."""

    def do_parse(self, line, expected, translation):
        """Test for word parsing."""
        word = Word.from_slovnik(line)
        self.assertEqual(word.word, expected)
        self.assertEqual(word.translation, translation)
        return word

    def test_parse(self) -> None:
        """Testing various weird stuff in parser."""
        word = self.do_parse("a\tb\ttype\tnote\tauthor", "a", "b")
        self.assertEqual(word.wtype, "type")
        self.assertEqual(word.note, "note")
        self.assertEqual(word.author, "author")

    def test_fixups(self) -> None:
        """Test for parsing fixups."""
        self.do_parse("a\tc\tb\ttype\tnote\tauthor", "ac", "b")
        self.do_parse("a\tb\ttype\tnote", "a", "b")
        self.do_parse("a\tb\ttype", "a", "b")
        self.do_parse("a\tb", "a", "b")
        self.do_parse("a", "a", "")

    def test_no_fixup(self) -> None:
        """Test for not detected fixup."""
        self.assertRaisesRegex(
            ValueError,
            r"Invalid input: \'\\t\\t\\t\\t\\t\\t\\t\\t\'",
            self.do_parse,
            "\t\t\t\t\t\t\t\t",
            "",
            "",
        )
