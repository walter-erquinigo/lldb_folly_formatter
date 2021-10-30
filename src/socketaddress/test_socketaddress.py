#!/usr/bin/env python3

from common import LLDBTestCase
from os import path

class FollySocketAddress(LLDBTestCase):
    def get_formatter_path(self):
        curr_dir = path.abspath(path.dirname(path.realpath(__file__)))
        return path.join(curr_dir, "socketaddress_formatter.py")

    def test_socketaddress(self):
        script = """
b socketaddress.cpp:8
r
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
(folly::SocketAddress) sock = (folly::SocketAddress) 10.0.0.10:3000
(folly::SocketAddress) $0 = (folly::SocketAddress) 10.0.0.10:3000
10.0.0.10:3000
(folly::SocketAddress) sock = (folly::SocketAddress) 192.168.0.1:4000
(folly::SocketAddress) $1 = (folly::SocketAddress) 192.168.0.1:4000
192.168.0.1:4000
(folly::SocketAddress) sock = (folly::SocketAddress) [0000:0000:0000:0000:0000:0000:0000:0001]:5000
(folly::SocketAddress) $2 = (folly::SocketAddress) [0000:0000:0000:0000:0000:0000:0000:0001]:5000
[::1]:5000
(folly::SocketAddress) sock = (folly::SocketAddress) [2620:0000:1cfe:face:b00c:0000:0000:0003]:6000
(folly::SocketAddress) $3 = (folly::SocketAddress) [2620:0000:1cfe:face:b00c:0000:0000:0003]:6000
[2620:0:1cfe:face:b00c::3]:6000
""".strip()

        self.assertEqual(expected, self.run_lldb("socketaddress", script))