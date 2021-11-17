import os
import lldb

# def summary(valueobj, dict):
#     print(valueobj
#         .GetChildMemberWithName('list_')
#         .GetChildMemberWithName('head_')
#     )
#     pass

class AtomicLLSyntheticFormatter:
    count = None

    def __init__(self, valobj, dict):
        self.valobj = valobj
    
    def next_node(self, node):
        return node.GetChildMemberWithName('next')

    def num_children(self):
        if self.count is None:
            self.count = self.num_children_impl()
        return self.count

    def num_children_impl(self):
        return 3
        try:
            # After a std::list has been initialized, both next and prev will
            # be non-NULL
            next_val = self._head.GetValueAsUnsigned(0)
            if next_val == 0: 
                return 0
            if self.has_loop():
                return 0
            if self.has_prev:
                prev_val = self.prev.GetValueAsUnsigned(0)
                if prev_val == 0:
                    return 0
                if next_val == self.node_address:
                    return 0
                if next_val == prev_val:
                    return 1   
            size = 1
            current = self._head
            while current.GetChildMemberWithName('next').GetValueAsUnsigned(0) != self.get_end_of_list_address():
                size = size + 1
                current = current.GetChildMemberWithName('next')
            return size 
        except:
            return 0

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
            offset = index
            current = self._head
            while offset > 0:
                current = self.next_node(current)
                offset = offset - 1
                
            child = current.CreateChildAtOffset(
                f'[{index}]', 
                self.data_size, 
                self.data_type)
            
            return child
        except:
            return None

    def extract_type(self):
        list_type = self.valobj.GetType().GetUnqualifiedType()
        if list_type.IsReferenceType():
            list_type = list_type.GetDereferencedType()
        if list_type.GetNumberOfTemplateArguments() > 0:
            data_type = list_type.GetTemplateArgumentType(0)
        else:
            data_type = None
        return data_type

    def update(self):
        try:
            self._head = (self.valobj
                .GetChildMemberWithName('list_')
                    .GetChildMemberWithName('head_')
                        .GetChildMemberWithName('_M_b')
                            .GetChildMemberWithName('_M_p')
                                )
            self.data_type = self.extract_type()
            self.data_size = self._head.GetType().GetByteSize()
            
            # If valid, continue
            if self._head.IsValid():
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
    typeName = r"(^folly::AtomicLinkedList<.*$)"
    moduleName = os.path.splitext(os.path.basename(__file__))[0]

    debugger.HandleCommand(
        'type synthetic add -x "' 
        + typeName + 
        '" --python-class '
        + moduleName 
        + '.AtomicLLSyntheticFormatter')

    # debugger.HandleCommand(
    #     'type summary add -x "'
    #     + typeName
    #     + '" --python-function '
    #     + moduleName
    #     + ".summary"
    # )
