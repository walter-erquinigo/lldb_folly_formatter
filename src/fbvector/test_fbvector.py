from common import LLDBTestCase
from os import path

class FollyFBVectorTest(LLDBTestCase):
    def get_formatter_path(self):
        curr_dir = path.abspath(path.dirname(path.realpath(__file__)))
        return path.join(curr_dir, "fbvector_formatter.py")

    def test_fbvector(self):
        script = """
b fbvector.cpp:9
r
script lldb.debugger.HandleCommand("frame var fbvec")
script lldb.debugger.HandleCommand("p fbvec")
c
script lldb.debugger.HandleCommand("frame var fbvec")
script lldb.debugger.HandleCommand("p fbvec")
c
script lldb.debugger.HandleCommand("frame var fbvec")
script lldb.debugger.HandleCommand("p fbvec")
c
script lldb.debugger.HandleCommand("frame var fbvec")
script lldb.debugger.HandleCommand("p fbvec")
c
script lldb.debugger.HandleCommand("frame var fbvec")
script lldb.debugger.HandleCommand("p fbvec")
c
script lldb.debugger.HandleCommand("frame var fbvec")
script lldb.debugger.HandleCommand("p fbvec")
c
script lldb.debugger.HandleCommand("frame var fbvec")
script lldb.debugger.HandleCommand("p fbvec")
c
"""

        expected = """
(folly::fbvector<unsigned int, std::allocator<> >) fbvec = size=0 {}
(folly::fbvector<unsigned int, std::allocator<> >) $0 = size=0 {}
(folly::fbvector<int, std::allocator<> >) fbvec = size=5 {
(int) [0] = 1
(int) [1] = 2
(int) [2] = 3
(int) [3] = 4
(int) [4] = 5
}
(folly::fbvector<int, std::allocator<> >) $1 = size=5 {
(int) [0] = 1
(int) [1] = 2
(int) [2] = 3
(int) [3] = 4
(int) [4] = 5
}
(folly::fbvector<double, std::allocator<> >) fbvec = size=4 {
(double) [0] = 1
(double) [1] = 2
(double) [2] = 3
(double) [3] = 4
}
(folly::fbvector<double, std::allocator<> >) $2 = size=4 {
(double) [0] = 1
(double) [1] = 2
(double) [2] = 3
(double) [3] = 4
}
(folly::fbvector<char, std::allocator<> >) fbvec = size=3 {
(char) [0] = 'A'
(char) [1] = 'B'
(char) [2] = 'C'
}
(folly::fbvector<char, std::allocator<> >) $3 = size=3 {
(char) [0] = 'A'
(char) [1] = 'B'
(char) [2] = 'C'
}
(folly::fbvector<bool, std::allocator<> >) fbvec = size=2 {
(bool) [0] = true
(bool) [1] = false
}
(folly::fbvector<bool, std::allocator<> >) $4 = size=2 {
(bool) [0] = true
(bool) [1] = false
}
(folly::fbvector<unsigned char, std::allocator<> >) fbvec = size=4 {
(unsigned char) [0] = '\n'
(unsigned char) [1] = '\v'
(unsigned char) [2] = '\f'
(unsigned char) [3] = '\r'
}
(folly::fbvector<unsigned char, std::allocator<> >) $5 = size=4 {
(unsigned char) [0] = '\n'
(unsigned char) [1] = '\v'
(unsigned char) [2] = '\f'
(unsigned char) [3] = '\r'
}
(folly::fbvector<float, std::allocator<> >) fbvec = size=4 {
(float) [0] = 1
(float) [1] = 2
(float) [2] = 3
(float) [3] = 4
}
(folly::fbvector<float, std::allocator<> >) $6 = size=4 {
(float) [0] = 1
(float) [1] = 2
(float) [2] = 3
(float) [3] = 4
}
""".strip()

        self.assertEqual(expected, self.run_lldb("fbvector", script))
