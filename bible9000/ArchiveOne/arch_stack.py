import sys
if '..' not in sys.path:
    sys.path.append('..')

from ArchiveOne.arch_verse import *
from ArchiveOne.arch_shelf import *

class ArchStack(ArchVersion):
    
    def __init__(self, ver:float=0, short_name:str='', desc:str='', code=0):
        super().__init__(ver, short_name, desc, code)
        self.__shelves = list()

    def get_shelfs(self):
        return list(self.__shelves) # mod the shelfs, not my list.

    def append_shelf(self, a_shelf)->int:
        ''' The shelf should be and instace of Archiveshelf, please. '''
        if not isinstance(a_shelf, ArchShelf):
            return -1
        self.__shelves.append(ArchShelf.Clone(a_shelf)) # precious
        return len(self.__shelves)

    def remove_shelf(self, shelf_num):
        ''' Remove a ones-based shelf identifier from the list. '''
        if shelf_num < 1 or shelf_num > len(self.__shelves):
            return None
        return self.__shelves.pop(shelf_num - 1)

    @staticmethod
    def Clone(obj):
        ''' Returns an instance if it gets one, else None. '''
        result = None
        if isinstance(obj, ArchStack):
            result = ArchShelf()
            result.__dict__ = dict(obj.__dict__) # clone it
        elif isinstance(obj, dict):
            result = ArchStack()
            if set(obj) != set(result.__dict__):
                return None
            result.__dict__ = dict(obj) # clone it
        return result


if __name__ == '__main__':
    sut = ArchStack(0.1, 'basic shelf', 'Just passin thru'); test_case = 10
    for i in range(test_case):
        a = ArchShelf(0.1, 'basic shelf', '''Just shelfin' thru''')
        if sut.append_shelf(a) != len(sut.get_shelfs()):
            print("Error 1000.")
            break
    
    if not len(sut.get_shelfs()) == test_case:
        print("Error 1010.")
    for _ in range(test_case):
        goober = sut.remove_shelf(1)
        del goober
    if len(sut.get_shelfs()) == 0:
        print("Testing Success!")
    else:
        for v in sut.get_shelfs():
            print(v.shelf_name)
            print(str(v.__dict__))
    

