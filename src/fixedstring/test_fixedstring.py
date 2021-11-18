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
b fixedstring.cpp:14
r
script lldb.debugger.HandleCommand("frame var str")
script lldb.debugger.HandleCommand("p str")
script lldb.debugger.HandleCommand("frame var empty")
script lldb.debugger.HandleCommand("p empty")
script lldb.debugger.HandleCommand("frame var longstr")
script lldb.debugger.HandleCommand("p longstr")
c
"""
        expected = """
abcdefghij
abcdefghijabcdefghijabcdefghijabcdefghijabcdefghij
(folly::FixedString<10>) str = "abcdefghij"
(folly::FixedString<10>) $0 = "abcdefghij"
(folly::FixedString<10>) empty = ""
(folly::FixedString<10>) $1 = ""
(folly::FixedString<50>) longstr = "abcdefghijabcdefghijabcdefghijabcdefghijabcdefghij"
(folly::FixedString<50>) $2 = "abcdefghijabcdefghijabcdefghijabcdefghijabcdefghij"

""".strip()

        self.assertEqual(expected, self.run_lldb("fixedstring", script))
