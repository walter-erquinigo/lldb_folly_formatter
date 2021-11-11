# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.

import lldb

def summary(valobj, dict):
    if not (valobj.IsValid()):
        return "<invalid>"

    # fbstring uses a union that is distinguished with a mask. If the string
    # is short, then no pointers are created and the string is stored in place.
    # Otherwise, a char * is created to hold the data. This formatter should
    # account for that.

    maskSize = valobj.GetTarget().FindFirstType("size_t").GetByteSize()
    catmask = 0xC0000000 if (maskSize == 4) else 0xC000000000000000
    capacity = (
        valobj.GetChildMemberWithName("store_")
        .GetChildMemberWithName("ml_")
        .GetChildMemberWithName("capacity_")
        .GetValueAsUnsigned()
    )

    category = capacity & catmask
    store = valobj.GetChildAtIndex(0)

    if category == 0:
        string = store.EvaluateExpression('(char *)small_')
    else:
        ml = store.GetChildMemberWithName("ml_")
        size = ml.GetChildMemberWithName("size_").GetValueAsUnsigned()
        if size > capacity:
            return "<invalid>"

        string = ml.GetChildMemberWithName("data_")

    summary = string.GetSummary()
    if summary is None:
        return str(string)
    return "(folly::fbstring) " + summary

def __lldb_init_module(debugger, internal_dict):
    typeName = "^(folly|std)::fbstring"
    functionName = f"{__name__}.summary"

    lldb.debugger.HandleCommand(
        'type summary add -x "'
        + typeName
        + '" --python-function '
        + functionName
    )
