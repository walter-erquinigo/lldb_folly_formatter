#!/usr/bin/env python3

from common import LLDBTestCase
from os import path

class FollyFixedStringTest(LLDBTestCase):
    def get_formatter_path(self):
        curr_dir = path.abspath(path.dirname(path.realpath(__file__)))
        return path.join(curr_dir, "fixedstring_formatter.py")

    def test_fixedstring(self):
        """
        This test makes sure that the fixedstring formatter works correctly.
        """

        script = """
b fixedstring.cpp:9
r
script lldb.debugger.HandleCommand("frame var str")
script lldb.debugger.HandleCommand("p str")
c
"""
        expected = """
abcdefghij
(folly::FixedString<10>) str = [10] "abcdefghij"
(folly::FixedString<10>) $0 = [10] "abcdefghij"
""".strip()

        self.assertEqual(expected, self.run_lldb("fixedstring", script))
