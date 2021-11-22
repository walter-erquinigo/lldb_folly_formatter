import	os
import	lldb
import	re

class ConcurrentBitsFormatter:
	def __init__(self, valobj,	dict):
		self.valobj = lldb.value(valobj)
		self.size = 0

		nTypeArgs = self.valobj.sbvalue.GetType().GetNumberOfTemplateArguments()
		typeName = self.valobj.sbvalue.GetType().GetDisplayTypeName()
		try:
			self.size = int(re.search('<(.+?)>', typeName).group(nTypeArgs))
		except AttributeError:
			pass

		self.blocktype = self.valobj.data_._M_elems[0]._M_i.sbvalue.GetType()
		self.blocksize = self.blocktype.GetCanonicalType().GetByteSize()

	def num_children(self):
		return self.size

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
			blockIndex = index // (self.blocksize * 8)
			block = self.valobj.data_._M_elems[blockIndex]._M_i
			# convert to int value for calculation
			binVal = block.sbvalue.GetValueAsUnsigned(0)

			binOffset = index % (self.blocksize * 8)
			binVal = 1 & (binVal >> binOffset)

			# create a `SBData` object from the value
			valDataArgs = [lldb.eByteOrderLittle, self.blocksize, [binVal]]
			valData = lldb.SBData_CreateDataFromUInt64Array(*valDataArgs)
			if self.blocksize == 4:
				valData = lldb.SBData_CreateDataFromUInt32Array(*valDataArgs)

			# root is a copy of valobj to avoid changing the original
			root = self.valobj.sbvalue
			# create a `SBValue` object from the `SBData` object
			child = root.CreateValueFromData(
				f"[{index}]",
				valData,
				root.GetType().GetTemplateArgumentType(0)
			)

			child.SetFormat(lldb.eFormatDecimal)
			return child
		except:
			return None

	def update(self):
		try:
			self.kblocklen = len(self.valobj.data_._M_elems)
		except:
			pass
		return False

def __lldb_init_module(debugger, dict):
	typeName = r"(^folly::ConcurrentBitSet<.*$)"
	moduleName = os.path.splitext(os.path.basename(__file__))[0]

	debugger.HandleCommand(
		'type synthetic add ' 
		+ f'-x "{typeName}" '
		+ f'--python-class {moduleName}.ConcurrentBitsFormatter')

	debugger.HandleCommand(
		'type summary add --expand --hide-empty --no-value '	
		+ f'-x "{typeName}" '	
		+ f'--summary-string "size=${{svar%#}}"')
