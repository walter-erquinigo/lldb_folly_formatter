import os
import lldb

class SparseByteSetFormatter:
	def __init__(self, valobj, dict):
		self.valobj = valobj

	def get_child_index(self, name):
		byte = int(name)
		return self.sparse[byte]

	def num_children(self):
		return self.size
	
	def get_child_at_index(self, index):
		index = int(index)
		if index < 0:
			return None
		if index >= self.num_children():
			return None
		try:
			value = lldb.value(self.dense)[index].sbvalue
			value.SetFormat(11)
			return value
		except:
			return None

	def update(self):
		try:
			self.size = self.valobj.GetChildMemberWithName("size_").GetValueAsUnsigned()
			self.sparse = self.valobj.GetChildMemberWithName("sparse_")
			self.dense = self.valobj.GetChildMemberWithName("dense_")

			# In case we get some erronious value
			if self.size < 0:
				self.size = 0
		except:
			pass
		return False

	def has_children(self):
		return True


def __lldb_init_module(debugger, dict):
    typeName = r"(^folly::SparseByteSet$)"
    moduleName = os.path.splitext(os.path.basename(__file__))[0]

    debugger.HandleCommand(
        'type synthetic add '
        + f'-x "{typeName}" '
        + f'--python-class {moduleName}.SparseByteSetFormatter'
    )

    debugger.HandleCommand(
        'type summary add --expand ' 
        + f'-x "{typeName}" ' 
        + f'--summary-string "size=${{var.size_}}"'
    )
