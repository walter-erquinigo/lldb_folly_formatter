from common import LLDBTestCase
from os import path

class FollyRangeTest(LLDBTestCase):
    def get_formatter_path(self):
        curr_dir = path.abspath(path.dirname(path.realpath(__file__)))
        return path.join(curr_dir, "range_formatter.py")

    def test_range(self):
        script = """
b range.cpp:8
b range.cpp:14
b range.cpp:20
b range.cpp:26
b range.cpp:50
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
script lldb.debugger.HandleCommand("frame var range")
script lldb.debugger.HandleCommand("p range")
c
script lldb.debugger.HandleCommand("frame var range")
script lldb.debugger.HandleCommand("p range")
c
script lldb.debugger.HandleCommand("frame var range")
script lldb.debugger.HandleCommand("p range")
c
script lldb.debugger.HandleCommand("frame var byter")
script lldb.debugger.HandleCommand("p byter")
c
script lldb.debugger.HandleCommand("frame var byter")
script lldb.debugger.HandleCommand("p byter")
c
n
script lldb.debugger.HandleCommand("frame var EmptyRange")
script lldb.debugger.HandleCommand("p EmptyRange")
c
"""

        expected = """
(folly::StringPiece) str = "Hello"
(folly::StringPiece) $0 = "Hello"
Hello
(folly::StringPiece) str = "Hello, World!"
(folly::StringPiece) $1 = "Hello, World!"
Hello, World!
(folly::StringPiece) str = "1234567890"
(folly::StringPiece) $2 = "1234567890"
1234567890
(folly::StringPiece) str = "Test"
(folly::StringPiece) $3 = "Test"
Test
(folly::Range<const unsigned int *>) range = size=4
(folly::Range<const unsigned int *>) $4 = size=4
(folly::Range<const float *>) range = size=3
(folly::Range<const float *>) $5 = size=3
(folly::Range<const char32_t *>) range = size=2
(folly::Range<const char32_t *>) $6 = size=2
(folly::ByteRange) byter = size=13
(folly::ByteRange) $7 = size=13
(folly::MutableByteRange) byter = size=13
(folly::MutableByteRange) $8 = size=13
(const folly::Range<const int *>) EmptyRange = size=0
(const folly::Range<const int *>) $9 = size=0
""".strip()

        self.assertEqual(expected, self.run_lldb("range", script))
