# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.

import os
import lldb
import socket

'''
The following formatter works for both folly::SocketAddress and folly::IPAddress.
'''

def address_to_string(ipaddr):
    family = ipaddr.family_.sbvalue.GetValueAsUnsigned()
    result = ""
    if family == socket.AF_INET:
        addr = ipaddr.addr_.ipV4Addr.addr_.bytes_._M_elems
        for i in range(0, 4):
            result += "{:d}.".format(int(addr[i]))
    elif family == socket.AF_INET6:
        addr = ipaddr.addr_.ipV6Addr.addr_.bytes_._M_elems
        for i in range(0, 8):
            result += "{:02x}{:02x}:".format(int(addr[2 * i]), int(addr[2 * i + 1]))
    else:
        return "unknown address family {}".format(family)
    return result[:-1]


def summary(valobj, dict):
    if not (valobj.IsValid()):
        return "<invalid>"

    typeName = valobj.GetDisplayTypeName()

    try:
        if typeName == "folly::SocketAddress":
            external = valobj.GetChildMemberWithName("external_")
            if external.GetValueAsUnsigned() != 0:
                return "Unix domain socket"
            else:
                val = lldb.value(valobj)
                addr = val.storage_.addr
                family = addr.family_.sbvalue.GetValueAsUnsigned()
                result = "(folly::SocketAddress) "
                if family == socket.AF_INET6:
                    result += "[" + address_to_string(addr) + "]"
                else:
                    result += address_to_string(addr)

                result += ":{}".format(val.port_.sbvalue.GetValueAsUnsigned())
                return result
        elif typeName == "folly::IPAddress":
            result = "(folly::IPAddress) "
            val = lldb.value(valobj)
            result += address_to_string(val)
            return result
        else:
            return str(valobj)

    except Exception:
        return str(typeName)

def __lldb_init_module(debugger, dict):
    typeName = r"^folly::IPAddress$|^folly::SocketAddress$"
    moduleName = os.path.splitext(os.path.basename(__file__))[0]

    debugger.HandleCommand(
        'type summary add -x "'
        + typeName
        + '" --python-function '
        + moduleName
        + ".summary"
    )


