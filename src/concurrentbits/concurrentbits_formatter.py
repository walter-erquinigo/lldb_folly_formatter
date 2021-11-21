import	os
import	lldb

class ConcurrentBitsFormatter:
	count =	None

	def	__init__(self,	valobj,	dict):
		self.valobj	= lldb.value(valobj)

	def	value(self,	node):
		return	node.GetValueAsUnsigned()

	def	num_children(self):
		return self.kblocklen

	def	get_child_index(self, name):
		try:
			return int(name.lstrip('[').rstrip(']'))
		except:
			return -1

	def	get_child_at_index(self, index):
		if index < 0:
			return None
		if index >= self.num_children():
			return None
		try:
			# value = self.valobj.data_._M_elems[index]._M_i
			# value = value.sbvalue
			# value.SetFormat(2)
			# return value

			# root is a copy of valobj to avoid changing the original
			root = self.valobj.sbvalue
			child = root.CreateChildAtOffset(
				f"[{index}]",
				index * self.blocksize,
				self.blocktype
			)

			if index == 0:
				for i in range(38):
					child.SetFormat(i)
					print(child)

			child.SetFormat(24)
			return child
		except:
			return None

	def	update(self):
		try:
			# print(self.valobj.sbvalue.GetType().GetNumberOfTemplateArguments())
			# print(self.valobj.sbvalue.GetType().GetDisplayTypeName())
			
			self.kblocklen = len(self.valobj.data_._M_elems)
			self.blocktype = self.valobj.data_._M_elems[0]._M_i.sbvalue.GetType()
			self.blocksize = self.blocktype.GetCanonicalType().GetByteSize()
		except:
			pass

def	__lldb_init_module(debugger,	dict):
	typeName	=	r"(^folly::ConcurrentBitSet<.*$)"
	moduleName	=	os.path.splitext(os.path.basename(__file__))[0]

	debugger.HandleCommand(
		'type synthetic add ' 
		+ f'-x "{typeName}" '
		+ f'--python-class {moduleName}.ConcurrentBitsFormatter')

	debugger.HandleCommand(
		'type summary add --expand --hide-empty --no-value '	
		+	f'-x "{typeName}" '	
		+	f'--summary-string "size=${{svar%#}}"')
