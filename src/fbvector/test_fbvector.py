from common import LLDBTestCase
from os import path

class FollyFBVectorTest(LLDBTestCase):
    def get_formatter_path(self):
        curr_dir = path.abspath(path.dirname(path.realpath(__file__)))
        return path.join(curr_dir, "fbvector_formatter.py")

    def test_fbvector(self):
        script = """
b fbvector.cpp:10
"""

        expected = """
""".strip()

        self.assertEqual(expected, self.run_lldb("fbvector", script))
