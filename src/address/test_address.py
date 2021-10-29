#!/usr/bin/env python3

from common import LLDBTestCase
from os import path

class FollyAddress(LLDBTestCase):
    def get_formatter_path(self):
        curr_dir = path.abspath(path.dirname(path.realpath(__file__)))
        return path.join(curr_dir, "address_formatter.py")

    def test_address(self):
        script = """
b address.cpp:11
b address.cpp:16
b address.cpp:21
r
script lldb.debugger.HandleCommand("frame var ip4")
script lldb.debugger.HandleCommand("p ip4")
c
script lldb.debugger.HandleCommand("frame var ip4")
script lldb.debugger.HandleCommand("p ip4")
c
script lldb.debugger.HandleCommand("frame var ip6")
script lldb.debugger.HandleCommand("p ip6")
c
script lldb.debugger.HandleCommand("frame var ip6")
script lldb.debugger.HandleCommand("p ip6")
c
script lldb.debugger.HandleCommand("frame var sock")
script lldb.debugger.HandleCommand("p sock")
c
script lldb.debugger.HandleCommand("frame var sock")
script lldb.debugger.HandleCommand("p sock")
c
script lldb.debugger.HandleCommand("frame var sock")
script lldb.debugger.HandleCommand("p sock")
c
script lldb.debugger.HandleCommand("frame var sock")
script lldb.debugger.HandleCommand("p sock")
c
"""

        expected = """
(folly::IPAddress) ip4 = (folly::IPAddress) 10.0.0.10
(folly::IPAddress) $0 = (folly::IPAddress) 10.0.0.10
10.0.0.10
(folly::IPAddress) ip4 = (folly::IPAddress) 192.168.0.1
(folly::IPAddress) $1 = (folly::IPAddress) 192.168.0.1
192.168.0.1
(folly::IPAddress) ip6 = (folly::IPAddress) 0000:0000:0000:0000:0000:0000:0000:0001
(folly::IPAddress) $2 = (folly::IPAddress) 0000:0000:0000:0000:0000:0000:0000:0001
::1
(folly::IPAddress) ip6 = (folly::IPAddress) 2620:0000:1cfe:face:b00c:0000:0000:0003
(folly::IPAddress) $3 = (folly::IPAddress) 2620:0000:1cfe:face:b00c:0000:0000:0003
2620:0:1cfe:face:b00c::3
(folly::SocketAddress) sock = (folly::SocketAddress) 10.0.0.10:3000
(folly::SocketAddress) $4 = (folly::SocketAddress) 10.0.0.10:3000
10.0.0.10:3000
(folly::SocketAddress) sock = (folly::SocketAddress) 192.168.0.1:4000
(folly::SocketAddress) $5 = (folly::SocketAddress) 192.168.0.1:4000
192.168.0.1:4000
(folly::SocketAddress) sock = (folly::SocketAddress) [0000:0000:0000:0000:0000:0000:0000:0001]:5000
(folly::SocketAddress) $6 = (folly::SocketAddress) [0000:0000:0000:0000:0000:0000:0000:0001]:5000
[::1]:5000
(folly::SocketAddress) sock = (folly::SocketAddress) [2620:0000:1cfe:face:b00c:0000:0000:0003]:6000
(folly::SocketAddress) $7 = (folly::SocketAddress) [2620:0000:1cfe:face:b00c:0000:0000:0003]:6000
[2620:0:1cfe:face:b00c::3]:6000
""".strip()

        self.assertEquals(expected, self.run_lldb("address", script))