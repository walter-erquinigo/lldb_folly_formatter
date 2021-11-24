import os

class OptionalFormatter:
	def __init__(self, valobj, dict):
		self.valobj = valobj

	def get_child_index(self, name):
		return int(name)

	def num_children(self):
		if self.has_value:
			return 1
		return 0
	
	def get_child_at_index(self, index):
		if index < 0:
			return None
		if not self.has_value:
			return None
		
		value = (self.valobj
			.GetChildMemberWithName('storage_')
			.GetChildMemberWithName('value')
		)

		return value
		# child = value.CreateChildAtOffset('Value', 0, value.GetType())
		# return child
	
	def update(self):
		self.has_value = True if (self.valobj
			.GetChildMemberWithName('storage_')
			.GetChildMemberWithName('hasValue')
			.GetValueAsUnsigned()
		) != 0 else False

		return False

	def has_children(self):
		return True


def OptionalSummary(valobj, dict):
	hasValue = valobj.GetNumChildren() > 0
	return f"Has Value={'true' if hasValue else 'false'}"


def __lldb_init_module(debugger, dict):
    typeName = r"(^folly::Optional<.*$)"
    moduleName = os.path.splitext(os.path.basename(__file__))[0]

    debugger.HandleCommand(
        'type synthetic add '
        + f'-x "{typeName}" '
        + f'--python-class {moduleName}.OptionalFormatter'
    )

    debugger.HandleCommand(
        'type summary add --expand --hide-empty --no-value ' 
        + f'-x "{typeName}" ' 
        + f'--python-function {moduleName}.OptionalSummary'
    )
