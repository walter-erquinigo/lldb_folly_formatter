# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.

import os


def summary(valobj, dict):
    return SyntheticFormatter.summary(valobj)


class SyntheticFormatter:

    # Type codes that aren't primitive values
    ARRAY_TYPE_CODE = 1
    OBJECT_TYPE_CODE = 5

    # Type is defined in folly::dynamic as:
    #   enum Type {
    #     NULLT,
    #     ARRAY,
    #     BOOL,
    #     DOUBLE,
    #     INT64,
    #     OBJECT,
    #     STRING,
    #    };
    TYPE_MEMBERS = {
        0: 'nul',
        1: 'array',
        2: 'boolean',
        3: 'doubl',
        4: 'integer',
        5: 'objectBuffer',
        6: 'string'
    }

    def __init__(self, valobj, dict):
        self.valobj = valobj

    @staticmethod
    def summary(valobj):
        try:
            typeCode = SyntheticFormatter.get_type_code(valobj)
            data = SyntheticFormatter.get_data(valobj.GetNonSyntheticValue(), typeCode)
            if data is None or not(data.IsValid()):
                return "folly::dynamic <invalid>"

            summary = 'folly::dynamic'
            if typeCode == SyntheticFormatter.OBJECT_TYPE_CODE:
                # Object
                summary += '::object size=' + str(data.GetNumChildren())
                return summary
            elif typeCode == SyntheticFormatter.ARRAY_TYPE_CODE:
                # Array
                summary += '::array'

            # simple integral types
            dataSummary = data.GetSummary()
            summary += ' '
            if dataSummary is None:
                data = data.CreateValueFromData('', data.GetData(), data.GetType())
                summary += str(data)
            else:
                summary += dataSummary

            return summary

        except Exception:
            return 'folly::dynamic'

    @staticmethod
    def is_container_type(typeCode):
        return typeCode == SyntheticFormatter.OBJECT_TYPE_CODE or \
               typeCode == SyntheticFormatter.ARRAY_TYPE_CODE

    @staticmethod
    def get_type_code(valobj):
        type = valobj.GetNonSyntheticValue().GetChildMemberWithName("type_")
        if type is None or not(type.IsValid()):
            return -1

        typeCode = type.GetValueAsUnsigned()
        if typeCode > len(SyntheticFormatter.TYPE_MEMBERS):
            return -1

        return typeCode

    @staticmethod
    def get_data(valobj, typeCode):
        if typeCode < 0:
            return None

        # Returns the correct data member from the folly::dynamic's union
        # based on the dynamic's type.
        rawData = valobj.GetChildMemberWithName("u_")
        if rawData is None or not(rawData.IsValid()):
            return None

        data = rawData.GetChildMemberWithName(SyntheticFormatter.TYPE_MEMBERS[typeCode])
        if typeCode == SyntheticFormatter.OBJECT_TYPE_CODE:
            # Need to unpack object buffer.
            # The objectBuffer is actually a different type, we need to cast it to:
            #   folly::F14NodeMap<
            #       folly::dynamic,
            #       folly::dynamic,
            #       folly::detail::DynamicHasher,
            #       folly::detail::DynamicKeyEqual,
            #       std::allocator<std::pair<const folly::dynamic, folly::dynamic>>>
            realType = valobj.GetTarget().FindFirstType(
                'folly::F14NodeMap<folly::dynamic, folly::dynamic, ' +
                'folly::detail::DynamicHasher, ' +
                'folly::detail::DynamicKeyEqual, ' +
                'std::allocator<' +
                'std::pair<const folly::dynamic, folly::dynamic> > >')
            return data.CreateValueFromData('entries', data.GetData(), realType)
        elif typeCode == SyntheticFormatter.ARRAY_TYPE_CODE:
            return data.CreateValueFromData('entries', data.GetData(), data.GetType())
        else:
            return data

    def num_children(self):
        typeCode = SyntheticFormatter.get_type_code(self.valobj)
        if SyntheticFormatter.is_container_type(typeCode):
            data = SyntheticFormatter.get_data(self.valobj, typeCode)
            if data is None or not(data.IsValid()):
                return 0
            return data.GetNumChildren()

        return 0

    def has_children(self):
        return self.num_children() > 0

    def get_child_index(self, name):
        if not(self.has_children()):
            return None
        return 0

    def get_child_at_index(self, index):
        try:
            if not(self.valobj.IsValid()):
                return None

            typeCode = SyntheticFormatter.get_type_code(self.valobj)
            if typeCode < 0 or typeCode > len(self.TYPE_MEMBERS):
                # Invalid type.
                return None

            data = SyntheticFormatter.get_data(self.valobj, typeCode)
            if index >= self.num_children():
                return None
            return data.GetChildAtIndex(index)

        except Exception:
            pass
        return None

    def update(self):
        return True


def __lldb_init_module(debugger, dict):
    typeName = 'folly::dynamic'
    moduleName = os.path.splitext(os.path.basename(__file__))[0]

    debugger.HandleCommand('type synthetic add "' + typeName + '" --python-class '
                           + moduleName + '.SyntheticFormatter')

    debugger.HandleCommand('type summary add "' + typeName + '" --python-function '
                           + moduleName + '.summary')


