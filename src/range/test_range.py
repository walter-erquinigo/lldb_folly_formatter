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
n
script lldb.debugger.HandleCommand("frame var EmptyRange")
script lldb.debugger.HandleCommand("p EmptyRange")
c
"""

        expected = """
(folly::StringPiece) str = (folly::StringPiece) "Hello"
(folly::StringPiece) $0 = (folly::StringPiece) "Hello"
Hello
(folly::StringPiece) str = (folly::StringPiece) "Hello, World!"
(folly::StringPiece) $1 = (folly::StringPiece) "Hello, World!"
Hello, World!
(folly::StringPiece) str = (folly::StringPiece) "1234567890"
(folly::StringPiece) $2 = (folly::StringPiece) "1234567890"
1234567890
(folly::StringPiece) str = (folly::StringPiece) "Test"
(folly::StringPiece) $3 = (folly::StringPiece) "Test"
Test
(folly::Range<const unsigned int *>) range = (folly::Range) <const unsigned int *> [4]
(folly::Range<const unsigned int *>) $4 = (folly::Range) <const unsigned int *> [4]
(folly::Range<const float *>) range = (folly::Range) <const float *> [3]
(folly::Range<const float *>) $5 = (folly::Range) <const float *> [3]
(folly::Range<const char32_t *>) range = (folly::Range) <const char32_t *> [2]
(folly::Range<const char32_t *>) $6 = (folly::Range) <const char32_t *> [2]
(folly::ByteRange) byter = (folly::Range) <const unsigned char *> [13]
(folly::ByteRange) $7 = (folly::Range) <const unsigned char *> [13]
(folly::MutableByteRange) byter = (folly::Range) <unsigned char *> [13]
(folly::MutableByteRange) $8 = (folly::Range) <unsigned char *> [13]
(const folly::Range<const int *>) EmptyRange = (folly::Range) <const int *> [0]
(const folly::Range<const int *>) $9 = (folly::Range) <const int *> [0]
""".strip()

        self.assertEqual(expected, self.run_lldb("range", script))
