from unittest import TestCase

from tests.helpers import strip_whitespace


class HelpersTests(TestCase):

    def test_stripWhitespace(self):
        self.assertEqual('abc', strip_whitespace('a b c'))
        self.assertEqual('abc', strip_whitespace(' a b c '))
        self.assertEqual('abc', strip_whitespace('   ab c '))
        self.assertEqual('abc', strip_whitespace('ab\nc'))
