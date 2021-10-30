#!/usr/bin/env python3

from common import LLDBTestCase
from os import path

class FollyAddress(LLDBTestCase):
    def get_formatter_path(self):
        curr_dir = path.abspath(path.dirname(path.realpath(__file__)))
        return path.join(curr_dir, "address_formatter.py")

    def test_address(self):
        script = """
b address.cpp:8
r
script lldb.debugger.HandleCommand("frame var ip")
script lldb.debugger.HandleCommand("p ip")
c
script lldb.debugger.HandleCommand("frame var ip")
script lldb.debugger.HandleCommand("p ip")
c
script lldb.debugger.HandleCommand("frame var ip")
script lldb.debugger.HandleCommand("p ip")
c
script lldb.debugger.HandleCommand("frame var ip")
script lldb.debugger.HandleCommand("p ip")
c
"""

        expected = """
(folly::IPAddress) ip = (folly::IPAddress) 10.0.0.10
(folly::IPAddress) $0 = (folly::IPAddress) 10.0.0.10
10.0.0.10
(folly::IPAddress) ip = (folly::IPAddress) 192.168.0.1
(folly::IPAddress) $1 = (folly::IPAddress) 192.168.0.1
192.168.0.1
(folly::IPAddress) ip = (folly::IPAddress) 0000:0000:0000:0000:0000:0000:0000:0001
(folly::IPAddress) $2 = (folly::IPAddress) 0000:0000:0000:0000:0000:0000:0000:0001
::1
(folly::IPAddress) ip = (folly::IPAddress) 2620:0000:1cfe:face:b00c:0000:0000:0003
(folly::IPAddress) $3 = (folly::IPAddress) 2620:0000:1cfe:face:b00c:0000:0000:0003
2620:0:1cfe:face:b00c::3
""".strip()

        self.assertEqual(expected, self.run_lldb("address", script))