from common import LLDBTestCase
from os import path

class FollyAtomicLLTest(LLDBTestCase):
    def get_formatter_path(self):
        curr_dir = path.abspath(path.dirname(path.realpath(__file__)))
        return path.join(curr_dir, "atomicll_formatter.py")

    def test_atomicll(self):
        curr_dir = path.abspath(path.dirname(path.realpath(__file__)))
        script = f"""
command script import {path.join(curr_dir, '..', "address/address_formatter.py")}
b atomicll.cpp:9
b atomicll.cpp:12
b atomicll.cpp:14
b atomicll.cpp:16
r
script lldb.debugger.HandleCommand("frame var ll")
script lldb.debugger.HandleCommand("p ll")
c
script lldb.debugger.HandleCommand("frame var ll")
script lldb.debugger.HandleCommand("p ll")
c
script lldb.debugger.HandleCommand("frame var li")
script lldb.debugger.HandleCommand("p li")
c
script lldb.debugger.HandleCommand("frame var li")
script lldb.debugger.HandleCommand("p li")
c
"""

        expected = """
(folly::AtomicLinkedList<char>) ll = size=0
(folly::AtomicLinkedList<char>) $0 = size=0
(folly::AtomicLinkedList<char>) ll = size=3 {
[0] = 'C'
[1] = 'B'
[2] = 'A'
}
(folly::AtomicLinkedList<char>) $1 = size=3 {
[0] = 'C'
[1] = 'B'
[2] = 'A'
}
(folly::AtomicLinkedList<folly::IPAddress>) li = size=0
(folly::AtomicLinkedList<folly::IPAddress>) $2 = size=0
(folly::AtomicLinkedList<folly::IPAddress>) li = size=2 {
[0] = (folly::IPAddress) 10.0.1.200
[1] = (folly::IPAddress) 10.0.0.100
}
(folly::AtomicLinkedList<folly::IPAddress>) $3 = size=2 {
[0] = (folly::IPAddress) 10.0.1.200
[1] = (folly::IPAddress) 10.0.0.100
}
""".strip()

        self.assertEqual(expected, self.run_lldb("atomicll", script))
