import os
import lldb

class AtomicLLSyntheticFormatter:
    count = None

    def __init__(self, valobj, dict):
        self.valobj = valobj
    
    def next_node(self, node):
        return (node
            .GetChildMemberWithName('hook')
                .GetChildMemberWithName('next')
        )

    def is_valid(self, node):
        return self.value(self.next_node(node)) != 0

    def value(self, node):
        return node.GetValueAsUnsigned()

    def num_children(self):
        if self.count is None:
            self.count = self.num_children_impl()
        return self.count

    def num_children_impl(self):
        try:
            next_val = self._head.GetValueAsUnsigned(0)
            if next_val == 0: 
                return 0
            if self.has_loop():
                return 0
            size = 1
            current = self._head
            while self.is_valid(current):
                size = size + 1
                current = self.next_node(current)
            return size 
        except:
            return 0
    
    # Floyd's cycle-finding algorithm
    # try to detect if this list has a loop
    def has_loop(self):
        slow = self._head
        fast1 = self._head
        fast2 = self._head
        while self.is_valid(slow):
            slow_value = self.value(slow)
            fast1 = self.next_node(fast2)
            fast2 = self.next_node(fast1)
            if self.value(fast1) == slow_value or self.value(
                    fast2) == slow_value:
                return True
            slow = self.next_node(slow)
        return False

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
                
            return current.CreateChildAtOffset(
                f'[{index}]', 
                self.data_size, 
                self.data_type)   
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
            self.next = self.next_node(self._head)
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
        'type synthetic add ' 
        + f'-x "{typeName}" '
        + f'--python-class {moduleName}.AtomicLLSyntheticFormatter')

    debugger.HandleCommand(
        'type summary add --expand --hide-empty --no-value ' 
        + f'-x "{typeName}" ' 
        + f'--summary-string "size=${{svar%#}}"'
    )
