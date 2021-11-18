from common import LLDBTestCase
from os import path

class FollyOptionalTest(LLDBTestCase):
    def get_formatter_path(self):
        curr_dir = path.abspath(path.dirname(path.realpath(__file__)))
        return path.join(curr_dir, "optional_formatter.py")

    def test_optional(self):
        curr_dir = path.abspath(path.dirname(path.realpath(__file__)))
        script = f"""
command script import {path.join(curr_dir, '..', "fbstring/fbstring_formatter.py")}
b optional.cpp:9
b optional.cpp:12
b optional.cpp:14
r
script lldb.debugger.HandleCommand("frame var someInt")
script lldb.debugger.HandleCommand("p someInt")
c
script lldb.debugger.HandleCommand("frame var someInt")
script lldb.debugger.HandleCommand("p someInt")
script lldb.debugger.HandleCommand("frame var someFbStr")
script lldb.debugger.HandleCommand("p someFbStr")
c
script lldb.debugger.HandleCommand("frame var someFbStr")
script lldb.debugger.HandleCommand("p someFbStr")
c
"""

        expected = """
(folly::Optional<int>) someInt = null
(folly::Optional<int>) $0 = null
(folly::Optional<int>) someInt = (int) value = 34
(folly::Optional<int>) $1 = (int) value = 34
(folly::Optional<folly::basic_fbstring<char, std::char_traits<char>, std::allocator<>, folly::fbstring_core<char> > >) someFbStr = null
(folly::Optional<folly::basic_fbstring<char, std::char_traits<char>, std::allocator<>, folly::fbstring_core<char> > >) $2 = null
(folly::Optional<folly::basic_fbstring<char, std::char_traits<char>, std::allocator<>, folly::fbstring_core<char> > >) someFbStr = (folly::basic_fbstring<char, std::char_traits<char>, std::allocator<>, folly::fbstring_core<char> >) value = (store_ = (folly::fbstring) "Hello, World!")
(folly::Optional<folly::basic_fbstring<char, std::char_traits<char>, std::allocator<>, folly::fbstring_core<char> > >) $4 = (folly::basic_fbstring<char, std::char_traits<char>, std::allocator<>, folly::fbstring_core<char> >) value = (store_ = (folly::fbstring) "Hello, World!")
""".strip()

        self.assertEqual(expected, self.run_lldb("optional", script))
