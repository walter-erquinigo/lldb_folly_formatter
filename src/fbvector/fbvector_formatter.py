# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.

# Similar implementation to the C++ std::vector formatter
# https://github.com/llvm-mirror/lldb/blob/master/examples/synthetic/gnu_libstdcpp.py

import os
import lldb

def summary(valobj, dict):
    vec = FBVectorFormatter(valobj)
    try:
        if not (valobj.IsValid()):
            return "<invalid>"

        # if FBVectorFormatter.is_string_piece(valobj):
        #     start = valobj.GetNonSyntheticValue().GetChildMemberWithName("b_")
        #     summary = start.GetSummary()
        #     if summary is None:
        #         return str(start)
        #     return summary
        # else:
        return f"size={vec.num_children()}"

    except Exception:
        return f"size={vec.num_children()}"


class FBVectorFormatter:
    def __init__(self, valobj):
        # logger = lldb.formatters.Logger.Logger()
        self.valobj = valobj
        self.count = None
    
    def num_children_impl(self):
        try:
            start_val = self.start.GetValueAsUnsigned(0)
            finish_val = self.finish.GetValueAsUnsigned(0)
            end_val = self.end.GetValueAsUnsigned(0)
            # Before a vector has been constructed, it will contain bad values
            # so we really need to be careful about the length we return since
            # uninitialized data can cause us to return a huge number. We need
            # to also check for any of the start, finish or end of storage values
            # being zero (NULL). If any are, then this vector has not been
            # initialized yet and we should return zero

            # Make sure nothing is NULL
            if start_val == 0 or finish_val == 0 or end_val == 0:
                return 0
            # Make sure start is less than finish
            if start_val >= finish_val:
                return 0
            # Make sure finish is less than or equal to end of storage
            if finish_val > end_val:
                return 0

            # if we have a struct (or other data type that the compiler pads to native word size)
            # this check might fail, unless the sizeof() we get is itself incremented to take the
            # padding bytes into account - on current clang it looks like
            # this is the case
            num_children = (finish_val - start_val)
            if (num_children % self.data_size) != 0:
                return 0
            else:
                num_children = num_children // self.data_size
            return num_children
        except:
            return 0

    def num_children(self):
        if self.count is None:
            self.count = self.num_children_impl()
        return self.count

    def get_child_index(self, name):
        try:
            return int(name.lstrip('[').rstrip(']'))
        except:
            return -1

    def get_child_at_index(self, index):
        # logger = lldb.formatters.Logger.Logger()
        # logger >> "Retrieving child " + str(index)
        if index < 0:
            return None
        if index >= self.num_children():
            return None
        try:
            offset = index * self.data_size
            return self.start.CreateChildAtOffset(
                '[' + str(index) + ']', offset, self.data_type)
        except:
            return None

    def update(self):
        self.count = None
        # preemptively setting this to None
        # we might end up changing our mind later

        try:
            impl = self.valobj.GetChildMemberWithName('_M_impl')
            self.start = impl.GetChildMemberWithName('_M_start')
            self.finish = impl.GetChildMemberWithName('_M_finish')
            self.end = impl.GetChildMemberWithName('_M_end_of_storage')
            self.data_type = self.start.GetType().GetPointeeType()
            self.data_size = self.data_type.GetByteSize()
            # if any of these objects is invalid, it means there is no
            # point in trying to fetch anything
            if self.start.IsValid() and self.finish.IsValid(
            ) and self.end.IsValid() and self.data_type.IsValid():
                self.count = None
            else:
                self.count = 0
        except:
            pass
        return True

    def has_children(self):
        return True

def __lldb_init_module(debugger, dict):
    typeName = r"^folly::fbvector<.*$"
    moduleName = os.path.splitext(os.path.basename(__file__))[0]

    debugger.HandleCommand(
        'type summary add -x "'
        + typeName
        + '" --python-function '
        + moduleName
        + ".summary"
    )