"""
Given two strings s and t, determine if they are isomorphic.
Two strings are isomorphic if the characters in s can be replaced to get t.

For example,"egg" and "add" are isomorphic, "foo" and "bar" are not.
"""

# My thought process:
# (0) Check that strings are the same length. Else False
# (1) walk down the strings together,
# (2) If char1 not in the map yet, add the mapping from char1 to char2
# (3) If char1 already in the map, it needs to match char2, else False

from unittest import TestCase


def are_isomorphic(string_1, string_2):

    if len(string_1) != len(string_2):
        return False

    char_map = {}

    for char_1, char_2 in zip(string_1, string_2):
        expected_char = char_map.get(char_1, None)
        if expected_char is None:
            char_map[char_1] = char_2
        else:
            if char_2 != expected_char:
                return False

    return True


class TestIso(TestCase):
    def test_iso(self):
        self.assertTrue(are_isomorphic("egg", "add"))
        self.assertFalse(are_isomorphic("foo", "bar"))
        self.assertFalse(are_isomorphic("foof", "baad"))
        self.assertTrue(are_isomorphic("eeggyff", "aaddyqq"))