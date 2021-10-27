# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.

import os
import lldb


def summary(valobj, dict):
    return SyntheticFormatter.summary(valobj)


def strip_template(typeName):
    templateStart = typeName.index("<")
    if templateStart > 0:
        return typeName[0:templateStart]
    return typeName


class SyntheticFormatter:

    def __init__(self, valobj, dict):
        try:
            self.valobj = valobj
            self._childCache = []
            self._table = self.valobj.GetChildMemberWithName('table_')

            # Determine what type of collection it is.
            typeName = self.valobj.GetDisplayTypeName()
            self._shortType = strip_template(typeName)
            self._isMap = "Map" in self._shortType
            self._isNode = "NodeContainer" in typeName
            self._enableIter = "VectorContainer" in self._table.GetDisplayTypeName()
        except Exception:
            pass

    @staticmethod
    def summary(valobj):
        try:
            table = valobj.GetNonSyntheticValue().GetChildMemberWithName('table_')
            summary = strip_template(valobj.GetDisplayTypeName())
            numChildren = SyntheticFormatter.num_children_table(table)
            summary += ' [' + str(numChildren) + ']'
            return summary
        except Exception:
            return 'folly::f14 Collection <unknown type>'

    @staticmethod
    def num_children_table(table):
        try:
            sizeAndPack = table.GetChildMemberWithName('sizeAndPackedBegin_')
            size = sizeAndPack.GetChildMemberWithName("size_")
            return size.GetValueAsUnsigned()
        except Exception:
            return 0

    def num_children(self):
        return SyntheticFormatter.num_children_table(self._table)

    def has_children(self):
        return True

    def get_child_index(self, name):
        return int(name[1:len(name)])

    def get_child_at_index(self, index):
        if not (self._table.IsValid()):
            return None

        try:
            if self._enableIter:
                return self.get_child_at_index_iterable(index)
            else:
                return self.get_child_at_index_non_iterable(index)
        except Exception:
            return None

    def get_child_at_index_iterable(self, index):
        try:
            itemType = self._table.GetType() \
                        .GetTemplateArgumentType(0) \
                        .GetTemplateArgumentType(0) \
                        .GetPointerType()
            values = lldb.value(self._table.GetChildMemberWithName('values_').Cast(itemType))
            return values[int(index)].sbvalue
        except Exception:
            return None

    def get_child_at_index_non_iterable(self, index):
        if len(self._childCache) == 0 and self.num_children() > 0:
            self.populate_children_non_iterable()
        if index > len(self._childCache):
            return None
        return self._childCache[index]

    def populate_children_non_iterable(self):
        # For Node and Value containers that don't have an iterator.
        try:
            table = self._table

            # Get a pointer to chunk, which is of type F14Chunk<Item>*
            chunkPtr = table.GetChildMemberWithName('chunks_')
            if chunkPtr is None:
                return None

            chunkCount = table.GetChildMemberWithName("chunkMask_").GetValueAsUnsigned() + 1

            # Get the item type from ChunkPtr, it's the template argument to (*ChunkPtr)'s type
            itemType = chunkPtr.Dereference().GetType().GetTemplateArgumentType(0)
            if itemType is None:
                return None

            if not((chunkCount & (chunkCount - 1)) == 0):
                # Chunk count is supposed to be a power of 2!
                return None

            chunkPtr = lldb.value(chunkPtr)

            # Walk through the table's chunks looking for chunks with data.
            childIndex = 0
            for chunkIndex in range(chunkCount):
                chunk = chunkPtr[chunkIndex]
                tags = chunk.tags_._M_elems
                rawItems = chunk.rawItems_._M_elems

                # Chunks can contain a different number of slots depending on the aligned
                # size of the table's items, so we need to look this up dynamically.
                chunkSlots = tags.sbvalue.GetType().GetByteSize()
                for i in range(chunkSlots):
                    tag = tags[i]
                    # Chunks with data have their tag top bit set
                    if tag & 0x80:
                        data = rawItems[i].sbvalue.GetChildMemberWithName('__data').Cast(itemType)
                        if self._isNode:
                            data = data.Dereference().Dereference()
                        else:
                            data = data.Dereference()

                        if self._isMap:
                            # If the type is a map, separate out the keys and values.
                            key = data.GetChildMemberWithName('first')
                            value = data.GetChildMemberWithName('second')
                            value = value.CreateValueFromData('data',
                                                              value.GetData(), value.GetType())
                            result = rawItems[i].sbvalue.CreateValueFromData('[' +
                                                                             str(key.GetSummary()) +
                                                                             ']',
                                                                             value.GetData(),
                                                                             value.GetType())

                        else:
                            # For Set types, list all children by index
                            result = rawItems[i].sbvalue.CreateValueFromData(
                                '[' + str(childIndex) + ']',
                                data.GetData(),
                                data.GetType())
                        childIndex += 1
                        self._childCache.append(result)

        except Exception:
            pass
        return None

    def update(self):
        self._table = self.valobj.GetChildMemberWithName('table_')
        self._childCache = []
        return True


def __lldb_init_module(debugger, dict):
    typeName = "(^folly::F14NodeMap<.*$)"
    typeName += "|(^folly::F14BasicMap<.*$)"
    typeName += "|(^folly::F14ValueMap<.*$)"
    typeName += "|(^folly::F14VectorMap<.*$)"
    typeName += "|(^folly::F14FastMap<.*$)"
    typeName += "|(^folly::F14NodeSet<.*$)"
    typeName += "|(^folly::F14ValueSet<.*$)"
    typeName += "|(^folly::F14VectorSet<.*$)"
    typeName += "|(^folly::F14FastSet<.*$)"
    moduleName = os.path.splitext(os.path.basename(__file__))[0]
    debugger.HandleCommand('type synthetic add -x "' + typeName + '" --python-class '
                           + moduleName + '.SyntheticFormatter')
    debugger.HandleCommand('type summary add -x "' + typeName + '" --python-function '
                           + moduleName + '.summary')


