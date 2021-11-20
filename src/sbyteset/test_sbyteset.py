from common import LLDBTestCase
from os import path

class FollySparseByteSetTest(LLDBTestCase):
    def get_formatter_path(self):
        curr_dir = path.abspath(path.dirname(path.realpath(__file__)))
        return path.join(curr_dir, "sbyteset_formatter.py")

    def test_sbyteset(self):
        curr_dir = path.abspath(path.dirname(path.realpath(__file__)))
        script = f"""
b sbyteset.cpp:10
b sbyteset.cpp:14
r
script lldb.debugger.HandleCommand("frame var set")
script lldb.debugger.HandleCommand("p set")
c
script lldb.debugger.HandleCommand("frame var set")
script lldb.debugger.HandleCommand("p set")
c
"""

        expected = """
(folly::SparseByteSet) set = size=0 {}
(folly::SparseByteSet) $0 = size=0 {}
(folly::SparseByteSet) set = size=3 {
[0] = 0xab
[1] = 0xcd
[2] = 0xef
}
(folly::SparseByteSet) $1 = size=3 {
[0] = 0xab
[1] = 0xcd
[2] = 0xef
}
0 1
""".strip()

        self.assertEqual(expected, self.run_lldb("sbyteset", script))
