from common import LLDBTestCase
from os import path

class FollyFBVectorTest(LLDBTestCase):
    def get_formatter_path(self):
        curr_dir = path.abspath(path.dirname(path.realpath(__file__)))
        return path.join(curr_dir, "fbvector_formatter.py")

    def test_fbvector(self):
        script = """
b fbvector.cpp:12
r
script lldb.debugger.HandleCommand("frame var Empty")
script lldb.debugger.HandleCommand("frame var Ints")
script lldb.debugger.HandleCommand("frame var Floats")
script lldb.debugger.HandleCommand("frame var Chars")
script lldb.debugger.HandleCommand("frame var Bools")
c
"""

        expected = """
(folly::fbvector<unsigned int, std::allocator<> >) Empty = size=0
(folly::fbvector<int, std::allocator<> >) Ints = size=5 {
[0] = 1
[1] = 2
[2] = 3
[3] = 4
[4] = 5
}
(folly::fbvector<float, std::allocator<> >) Floats = size=4 {
[0] = 1.5
[1] = 2.5
[2] = 3.5
[3] = 4.5
}
(folly::fbvector<char, std::allocator<> >) Chars = size=3 {
[0] = 'A'
[1] = 'B'
[2] = 'C'
}
(folly::fbvector<bool, std::allocator<> >) Bools = size=2 {
[0] = true
[1] = false
}
""".strip()

        self.assertEqual(expected, self.run_lldb("fbvector", script))
