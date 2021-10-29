from common import LLDBTestCase
from os import path

class FollyRangeTest(LLDBTestCase):
    def get_formatter_path(self):
        curr_dir = path.abspath(path.dirname(path.realpath(__file__)))
        return path.join(curr_dir, "range_formatter.py")

    def test_range(self):
        pass