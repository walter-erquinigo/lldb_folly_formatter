from common import LLDBTestCase
from os import path

class FollyConcurrentLazyTest(LLDBTestCase):
	def get_formatter_path(self):
		curr_dir = path.abspath(path.dirname(path.realpath(__file__)))
		return path.join(curr_dir, "concurrentlazy_formatter.py")

	def test_concurrentlazy(self):
		"""
		This test makes sure that the concurrentlazy formatter works correctly.
		"""

		script = """
b concurrentlazy.cpp:10
b concurrentlazy.cpp:15
r
script lldb.debugger.HandleCommand("frame var val")
script lldb.debugger.HandleCommand("p val")
c
script lldb.debugger.HandleCommand("frame var val")
script lldb.debugger.HandleCommand("p val")
c
		"""
		expected = """
(folly::ConcurrentLazy<(anonymous class)>) val = Is Computed=false
(folly::ConcurrentLazy<(anonymous class)>) $0 = Is Computed=false
Expensive Value: 11
Reused Value: 11
(folly::ConcurrentLazy<(anonymous class)>) val = Is Computed=true {
value = 11
}
(folly::ConcurrentLazy<(anonymous class)>) $1 = Is Computed=true {
value = 11
}
		""".strip()

		self.assertEqual(expected, self.run_lldb("concurrentlazy", script))
