import os
import lldb

class ConcurrentLazyFormatter:
	def __init__(self, valobj, dict):
		self.valobj = lldb.value(valobj)

	def get_child_index(self, name):
		return 0 # There is only ever one child

	def num_children(self):
		if self.has_value:
			return 1
		return 0
	
	def get_child_at_index(self, index):
		if index != 0:
			return None # There is only ever one child
		if not self.has_value:
			return None
		return self.valobj.value_.storage_.value.sbvalue
	
	def update(self):
		self.has_value = True if (
			self.valobj
				.value_
				.storage_
				.init
				.mutex_
				.lock_
			.sbvalue.GetValueAsUnsigned()
		) != 0 else False
		return False

	def has_children(self):
		return self.has_value


def ConcurrentLazySummary(valobj, _dict):
	computed = valobj.GetNumChildren() > 0;
	return f"Is Computed={'true' if computed else 'false'}"


def __lldb_init_module(debugger, _dict):
	typeName = r"(^folly::ConcurrentLazy<.*$)"
	moduleName = os.path.splitext(os.path.basename(__file__))[0]

	debugger.HandleCommand(
		'type synthetic add '
		+ f'-x "{typeName}" '
		+ f'--python-class {moduleName}.ConcurrentLazyFormatter'
	)

	debugger.HandleCommand(
		'type summary add --expand --hide-empty --no-value ' 
		+ f'-x "{typeName}" ' 
		+ f'--python-function {moduleName}.ConcurrentLazySummary'
	)
