from common import LLDBTestCase
from os import path

class FollyF14Test(LLDBTestCase):
    def get_formatter_path(self):
        curr_dir = path.abspath(path.dirname(path.realpath(__file__)))
        return path.join(curr_dir, "f14_formatter.py")

    def test_f14(self):
        script = """
b f14.cpp:12
r

c
"""

        expected = """
""".strip()

        self.assertEqual(expected, self.run_lldb("f14", script))
