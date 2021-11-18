import os

def summary(valobj, dict):
	try:
		if not (valobj.IsValid()):
			return "<invalid>"

		has_value = True if (valobj
			.GetChildMemberWithName('storage_')
			.GetChildMemberWithName('hasValue')
			.GetValue()
		) == 'true' else False
		
		if has_value:
			return (valobj
				.GetChildMemberWithName('storage_')
				.GetChildMemberWithName('value')
				# .GetValue()
			)
		else:
			return "null"
	except:
		pass
	return "<invalid>"

def __lldb_init_module(debugger, dict):
    typeName = r"(^folly::Optional<.*$)"
    moduleName = os.path.splitext(os.path.basename(__file__))[0]

    debugger.HandleCommand(
        'type summary add --hide-empty ' 
        + f'-x "{typeName}" ' 
        + f'--python-function "{moduleName}.summary"'
    )
