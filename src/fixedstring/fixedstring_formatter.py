import os

def summary(valobj, dict):
	try:
		if not (valobj.IsValid()):
			return "<invalid>"

		string = valobj.GetChildMemberWithName('data_').GetSummary()
		size = valobj.GetChildMemberWithName('size_').GetValue()

		return f'[{size}] {string}'
	except:
		pass
	return "<invalid>"

def __lldb_init_module(debugger, dict):
    typeName = r"(^folly::FixedString<.*$)"
    moduleName = os.path.splitext(os.path.basename(__file__))[0]

    debugger.HandleCommand(
        'type summary add --hide-empty ' 
        + f'-x "{typeName}" ' 
        + f'--python-function "{moduleName}.summary"'
    )
