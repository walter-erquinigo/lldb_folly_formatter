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
script lldb.debugger.HandleCommand("p str")
c
script lldb.debugger.HandleCommand("frame var str")
script lldb.debugger.HandleCommand("p str")
c
script lldb.debugger.HandleCommand("frame var str")
script lldb.debugger.HandleCommand("p str")
c
script lldb.debugger.HandleCommand("frame var str")
script lldb.debugger.HandleCommand("p str")
c
script lldb.debugger.HandleCommand("frame var str")
script lldb.debugger.HandleCommand("p str")
c
script lldb.debugger.HandleCommand("frame var str")
script lldb.debugger.HandleCommand("p str")
c
script lldb.debugger.HandleCommand("frame var str")
script lldb.debugger.HandleCommand("p str")
c
"""
        expected = """
(folly::fbstring) str = (folly::fbstring) ""
(folly::fbstring) $1 = (folly::fbstring) ""

(folly::fbstring) str = (folly::fbstring) "a"
(folly::fbstring) $4 = (folly::fbstring) "a"
a
(folly::fbstring) str = (folly::fbstring) "aa"
(folly::fbstring) $7 = (folly::fbstring) "aa"
aa
(folly::fbstring) str = (folly::fbstring) "aaaaaaaaaaaaaaaaaaaaaaa"
(folly::fbstring) $10 = (folly::fbstring) "aaaaaaaaaaaaaaaaaaaaaaa"
aaaaaaaaaaaaaaaaaaaaaaa
(folly::fbstring) str = (folly::fbstring) "aaaaaaaaaaaaaaaaaaaaaaaa"
(folly::fbstring) $12 = (folly::fbstring) "aaaaaaaaaaaaaaaaaaaaaaaa"
aaaaaaaaaaaaaaaaaaaaaaaa
(folly::fbstring) str = (folly::fbstring) "aaaaaaaaaaaaaaaaaaaaaaaaa"
(folly::fbstring) $13 = (folly::fbstring) "aaaaaaaaaaaaaaaaaaaaaaaaa"
aaaaaaaaaaaaaaaaaaaaaaaaa
(folly::fbstring) str = (folly::fbstring) "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
(folly::fbstring) $14 = (folly::fbstring) "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
""".strip()

        self.assertEqual(expected, self.run_lldb("fbstring", script))
