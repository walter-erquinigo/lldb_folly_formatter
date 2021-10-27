#!/usr/bin/env python3

from common import LLDBTestCase
from os import path

class LLDBFollyTests(LLDBTestCase):
    def get_formatter_path(self):
        curr_dir = path.abspath(path.dirname(path.realpath(__file__)))
        return path.join(curr_dir, "fbstring_formatter.py")

    def test_fbstring(self):
        """
        This test makes sure that the fbstring formatter works correctly.
        """

        script = """
b fbstring.cpp:9
r
script lldb.debugger.HandleCommand("frame var str")
c
script lldb.debugger.HandleCommand("frame var str")
c
script lldb.debugger.HandleCommand("frame var str")
c
script lldb.debugger.HandleCommand("frame var str")
c
script lldb.debugger.HandleCommand("frame var str")
c
script lldb.debugger.HandleCommand("frame var str")
c
script lldb.debugger.HandleCommand("frame var str")
c
"""
        expected = """
(folly::fbstring) str = (folly::fbstring) ""

(folly::fbstring) str = (folly::fbstring) "a"
a
(folly::fbstring) str = (folly::fbstring) "aa"
aa
(folly::fbstring) str = (folly::fbstring) "aaaaaaaaaaaaaaaaaaaaaaa"
aaaaaaaaaaaaaaaaaaaaaaa
(folly::fbstring) str = (folly::fbstring) "aaaaaaaaaaaaaaaaaaaaaaaa"
aaaaaaaaaaaaaaaaaaaaaaaa
(folly::fbstring) str = (folly::fbstring) "aaaaaaaaaaaaaaaaaaaaaaaaa"
aaaaaaaaaaaaaaaaaaaaaaaaa
(folly::fbstring) str = (folly::fbstring) "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
""".strip()

        self.assertEqual(expected, self.run_lldb("fbstring", script))
