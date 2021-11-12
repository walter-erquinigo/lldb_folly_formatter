from common import LLDBTestCase
from os import path

class FollyF14Test(LLDBTestCase):
    def get_formatter_path(self):
        curr_dir = path.abspath(path.dirname(path.realpath(__file__)))
        return path.join(curr_dir, "f14_formatter.py")

    def test_f14(self):
        script = """
b f14.cpp:28
r
script lldb.debugger.HandleCommand("frame var fmap")
script lldb.debugger.HandleCommand("p fmap")
script lldb.debugger.HandleCommand("frame var fset")
script lldb.debugger.HandleCommand("p fset")
script lldb.debugger.HandleCommand("frame var nmap")
script lldb.debugger.HandleCommand("p nmap")
script lldb.debugger.HandleCommand("frame var nset")
script lldb.debugger.HandleCommand("p nset")
script lldb.debugger.HandleCommand("frame var vset")
script lldb.debugger.HandleCommand("p vset")
c
"""

        expected = """
(folly::F14FastMap<int, std::basic_string<>, folly::HeterogeneousAccessHash<int, void>, folly::HeterogeneousAccessEqualTo<int, void>, std::allocator<std::pair<const int, std::basic_string<> > > >) fmap = folly::F14FastMap [1]
(folly::F14FastMap<int, std::basic_string<>, folly::HeterogeneousAccessHash<int, void>, folly::HeterogeneousAccessEqualTo<int, void>, std::allocator<std::pair<const int, std::basic_string<> > > >) $0 = folly::F14FastMap [1]
(folly::F14FastSet<std::basic_string<>, folly::HeterogeneousAccessHash<std::basic_string<>, void>, folly::HeterogeneousAccessEqualTo<std::basic_string<>, void>, std::allocator<std::basic_string<> > >) fset = folly::F14FastSet [3]
(folly::F14FastSet<std::basic_string<>, folly::HeterogeneousAccessHash<std::basic_string<>, void>, folly::HeterogeneousAccessEqualTo<std::basic_string<>, void>, std::allocator<std::basic_string<> > >) $1 = folly::F14FastSet [3]
(folly::F14NodeMap<std::basic_string<>, std::basic_string<>, folly::HeterogeneousAccessHash<std::basic_string<>, void>, folly::HeterogeneousAccessEqualTo<std::basic_string<>, void>, std::allocator<std::pair<const std::basic_string<>, std::basic_string<> > > >) nmap = folly::F14NodeMap [1]
(folly::F14NodeMap<std::basic_string<>, std::basic_string<>, folly::HeterogeneousAccessHash<std::basic_string<>, void>, folly::HeterogeneousAccessEqualTo<std::basic_string<>, void>, std::allocator<std::pair<const std::basic_string<>, std::basic_string<> > > >) $2 = folly::F14NodeMap [1]
(folly::F14NodeSet<std::basic_string<>, folly::HeterogeneousAccessHash<std::basic_string<>, void>, folly::HeterogeneousAccessEqualTo<std::basic_string<>, void>, std::allocator<std::basic_string<> > >) nset = folly::F14NodeSet [1]
(folly::F14NodeSet<std::basic_string<>, folly::HeterogeneousAccessHash<std::basic_string<>, void>, folly::HeterogeneousAccessEqualTo<std::basic_string<>, void>, std::allocator<std::basic_string<> > >) $3 = folly::F14NodeSet [1]
(folly::F14ValueSet<float, folly::HeterogeneousAccessHash<float, void>, folly::HeterogeneousAccessEqualTo<float, void>, std::allocator<float> >) vset = folly::F14ValueSet [0]
(folly::F14ValueSet<float, folly::HeterogeneousAccessHash<float, void>, folly::HeterogeneousAccessEqualTo<float, void>, std::allocator<float> >) $4 = folly::F14ValueSet [0]
""".strip()

        self.assertEqual(expected, self.run_lldb("f14", script))
