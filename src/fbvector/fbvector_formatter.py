# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.

# Similar implementation to the C++ std::vector formatter
# https://github.com/llvm-mirror/lldb/blob/master/examples/synthetic/gnu_libstdcpp.py

import os
import lldb

class FBVectorFormatter:
    def __init__(self, valobj, dict):
        self.valobj = valobj
        self.count = None
        self.update()
    
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
        except Exception as e:
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
        if index < 0:
            return None
        if index >= self.num_children():
            return None
        try:
            return lldb.value(self.start)[int(index)].sbvalue
        except:
            return None

    def update(self):
        try:
            impl = self.valobj.GetChildMemberWithName('impl_')
            self.start = impl.GetChildMemberWithName('b_')
            self.finish = impl.GetChildMemberWithName('e_')
            self.end = impl.GetChildMemberWithName('z_')
            self.data_type = self.start.GetType().GetPointeeType()
            self.data_size = self.data_type.GetByteSize()
            
            # If valid, continue
            if self.start.IsValid() and self.finish.IsValid(
            ) and self.end.IsValid() and self.data_type.IsValid():
                self.count = None
            # if any of these objects is invalid, it means there is no
            # point in trying to fetch anything
            else:
                self.count = 0
        except:
            pass
        return False

    def has_children(self):
        return True


def __lldb_init_module(debugger, dict):
    typeName = r"^folly::fbvector<.*$"
    moduleName = os.path.splitext(os.path.basename(__file__))[0]

    debugger.HandleCommand(
        'type summary add --expand --hide-empty --no-value ' 
        + f'-x "{typeName}" ' 
        + f'--summary-string "size=${{svar%#}}"'
    )

    debugger.HandleCommand(
        'type synthetic add '
        + f'-x "{typeName}" '
        + f'-l {moduleName}.FBVectorFormatter'
    )
