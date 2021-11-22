from common import LLDBTestCase
from os import path

class FollyConcurrentBitSetTest(LLDBTestCase):
  def get_formatter_path(self):
    curr_dir = path.abspath(path.dirname(path.realpath(__file__)))
    return path.join(curr_dir, "concurrentbits_formatter.py")

  def test_concurrentbits(self):
    curr_dir = path.abspath(path.dirname(path.realpath(__file__)))
    script = f"""
b concurrentbits.cpp:15
r
script lldb.debugger.HandleCommand("frame var bits")
script lldb.debugger.HandleCommand("p bits")
script lldb.debugger.HandleCommand("frame var manybits")
script lldb.debugger.HandleCommand("p manybits")
c
"""

    expected = """
(folly::ConcurrentBitSet<8>) bits = size=8 {
[0] = 0
[1] = 1
[2] = 0
[3] = 1
[4] = 0
[5] = 1
[6] = 0
[7] = 1
}
(folly::ConcurrentBitSet<8>) $0 = size=8 {
[0] = 0
[1] = 1
[2] = 0
[3] = 1
[4] = 0
[5] = 1
[6] = 0
[7] = 1
}
(folly::ConcurrentBitSet<24>) manybits = size=24 {
[0] = 0
[1] = 0
[2] = 1
[3] = 0
[4] = 0
[5] = 1
[6] = 0
[7] = 0
[8] = 1
[9] = 0
[10] = 0
[11] = 1
[12] = 0
[13] = 0
[14] = 1
[15] = 0
[16] = 0
[17] = 1
[18] = 0
[19] = 0
[20] = 1
[21] = 0
[22] = 0
[23] = 1
}
(folly::ConcurrentBitSet<24>) $1 = size=24 {
[0] = 0
[1] = 0
[2] = 1
[3] = 0
[4] = 0
[5] = 1
[6] = 0
[7] = 0
[8] = 1
[9] = 0
[10] = 0
[11] = 1
[12] = 0
[13] = 0
[14] = 1
[15] = 0
[16] = 0
[17] = 1
[18] = 0
[19] = 0
[20] = 1
[21] = 0
[22] = 0
[23] = 1
}
""".strip()

    self.assertEqual(expected, self.run_lldb("concurrentbits", script))
