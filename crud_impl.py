# author Stoilov ( hardc0d3 )
# a little dirty implementation

from pysubject import SubjectOperation, Factory
import crud_interface

# mappings between interface and implementation wrapper

interface_to_subject = {
    'get': 'vl_get',
    'set': 'vl_set',
    'empty': 'vl_empty',
    'append': 'vl_append'
}

# exmaple implementation wrappers but using native not abstract operations

class ListWrap(list):
    def __init__(self, count):
        self.__iadd__([None]*count)

    def vl_get(self, index):
        return self.__getitem__(index)

    def vl_set(self, index, item):
        return self.__setitem__(index,item)

    def vl_empty(self):
        del self[:]

    def vl_append(self, item):
        return self.append(item)


class DictWrap(dict):
    def __init__(self):
        pass

    def vl_get(self, index):
        return self.__getitem__(index)

    def vl_set(self, index, item):
        return self.__setitem__(index,item)

    def vl_empty(self):
        self.clear()

    def vl_append(self, item):
        return self.vl_set(item, None)

# quick and dirty abstract implemented synchronous muxer
# using the pure abstract operational model
# that way with interchangeable implementations

class CrudMux(object):
    def __init__(self, c1, c2, c3):
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3

    def append(self,item):
        self.c1.append(item)
        self.c2.append(item)
        self.c3.append(item)

    def empty(self):
        self.c1.empty()
        self.c2.empty()
        self.c3.empty()


crud1 = crud_interface.CrudInterface()
crud2 = crud_interface.CrudInterface()
crud3 = crud_interface.CrudInterface()

mux = CrudMux(crud1, crud2, crud3) # tottaly abstract implemented

# impl factory
# SubjectOperation, may changes dynamically impl context

l1 = Factory(ListWrap, interface_to_subject, crud1, (0,), {})
l2 = Factory(ListWrap, interface_to_subject, crud2, (0,), {})
d3 = Factory(DictWrap, interface_to_subject, crud3, (), {})

# mux.append(item), mux.empty() apply to l1,l2,d3




