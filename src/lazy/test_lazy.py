from common import LLDBTestCase
from os import path

class FollyLazyTest(LLDBTestCase):
	def get_formatter_path(self):
		curr_dir = path.abspath(path.dirname(path.realpath(__file__)))
		return path.join(curr_dir, "lazy_formatter.py")

	def test_lazy(self):
		"""
		This test makes sure that the lazy formatter works correctly.
		"""

		script = """
b lazy.cpp:16
b lazy.cpp:21
r
script lldb.debugger.HandleCommand("frame var val")
script lldb.debugger.HandleCommand("p val")
c
script lldb.debugger.HandleCommand("frame var val")
script lldb.debugger.HandleCommand("p val")
c
		"""
		expected = """
(folly::detail::Lazy<(anonymous class)>) val = Is Computed=false {}
(folly::detail::Lazy<(anonymous class)>) $0 = Is Computed=false {}
Expensive Value: 11
Reused Value: 11
(folly::detail::Lazy<(anonymous class)>) val = Is Computed=true {
value = 11
}
(folly::detail::Lazy<(anonymous class)>) $1 = Is Computed=true {
value = 11
}
		""".strip()

		self.assertEqual(expected, self.run_lldb("lazy", script))
