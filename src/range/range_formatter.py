# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.

import os
import lldb


def summary(valobj, dict):
    try:
        if not (valobj.IsValid()):
            return "(folly::Range) <invalid>"

        if SyntheticFormatter.is_string_piece(valobj):
            start = valobj.GetNonSyntheticValue().GetChildMemberWithName("b_")
            summary = start.GetSummary()
            if summary is None:
                return str(start)
            return "(folly::StringPiece) " + summary
        else:
            return "folly::Range size=" + str(
                SyntheticFormatter.get_range_length(valobj)
            )

    except Exception:
        return "folly::Range"


class SyntheticFormatter:
    def __init__(self, valobj, dict):
        self.valobj = valobj

    @staticmethod
    def get_item_type(valobj):
        return valobj.GetType().GetTemplateArgumentType(0)

    @staticmethod
    def is_string_piece(valobj):
        typeName = valobj.GetDisplayTypeName()
        if typeName == "folly::StringPiece":
            return True

        return SyntheticFormatter.get_item_type(valobj) == "char*"

    @staticmethod
    def get_range_length(valobj):
        itemType = SyntheticFormatter.get_item_type(valobj).GetPointeeType()
        itemSize = itemType.GetByteSize()
        start = (
            valobj.GetNonSyntheticValue()
            .GetChildMemberWithName("b_")
            .GetValueAsUnsigned()
        )
        end = (
            valobj.GetNonSyntheticValue()
            .GetChildMemberWithName("e_")
            .GetValueAsUnsigned()
        )
        return (end - start) / itemSize

    def num_children(self):
        if SyntheticFormatter.is_string_piece(self.valobj):
            return 0
        return SyntheticFormatter.get_range_length(self.valobj)

    def has_children(self):
        return self.num_children() > 0

    def get_child_index(self, name):
        return int(name[1:len(name)])

    def get_child_at_index(self, index):
        begin = lldb.value(
            self.valobj.GetNonSyntheticValue().GetChildMemberWithName("b_")
        )
        return begin[int(index)].sbvalue

    def update(self):
        return True


def __lldb_init_module(debugger, dict):
    typeName = r"^folly::Range<.*$|^folly::StringPiece$"
    moduleName = os.path.splitext(os.path.basename(__file__))[0]

    debugger.HandleCommand(
        'type synthetic add -x "'
        + typeName
        + '" --python-class '
        + moduleName
        + ".SyntheticFormatter"
    )

    debugger.HandleCommand(
        'type summary add -x "'
        + typeName
        + '" --python-function '
        + moduleName
        + ".summary"
    )


