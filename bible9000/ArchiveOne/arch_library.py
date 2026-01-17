import sys
if '..' not in sys.path:
    sys.path.append('..')

''' 
Metaphore is:

ArchVerse   0..*:1 ArchBook
ArchBook    1..*:1 ArchShelf
ArchShelf   1..*:1 ArchStack
ArchStack   0..*:1 ArchLibrary

And everything has a version.
'''
from ArchiveOne.arch_verse import *
from ArchiveOne.arch_stack import *

class ArchLibrary(ArchVersion):
    
    def __init__(self, ver:float=0, short_name:str='', desc:str='', code=0):
        super().__init__(ver, short_name, desc, code)
        self.__racks = list()

    def get_racks(self):
        return list(self.__racks) # mod the racks, not my list.

    def append_rack(self, a_rack)->int:
        ''' The rack should be and instace of Archiverack, please. '''
        if not isinstance(a_rack, ArchStack):
            return -1
        self.__racks.append(ArchStack.Clone(a_rack)) # precious
        return len(self.__racks)

    def remove_rack(self, rack_num):
        ''' Remove a ones-based rack identifier from the list. '''
        if rack_num < 1 or rack_num > len(self.__racks):
            return None
        return self.__racks.pop(rack_num - 1)

    @staticmethod
    def Clone(obj):
        ''' Returns an instance if it gets one, else None. '''
        result = None
        if isinstance(obj, ArchLibrary):
            result = ArchLibrary()
            result.__dict__ = dict(obj.__dict__) # clone it
        elif isinstance(obj, dict):
            result = ArchLibrary()
            if set(obj) != set(result.__dict__):
                return None
            result.__dict__ = dict(obj) # clone it
        return result


if __name__ == '__main__':
    sut = ArchLibrary(0.1, 'basic rack', 'Just passin thru'); test_case = 10
    for i in range(test_case):
        a = ArchStack(0.1, 'basic rack', '''Just rackin' thru''')
        if sut.append_rack(a) != len(sut.get_racks()):
            print("Error 1000.")
            break
    
    if not len(sut.get_racks()) == test_case:
        print("Error 1010.")
    for _ in range(test_case):
        goober = sut.remove_rack(1)
        del goober
    if len(sut.get_racks()) == 0:
        print("Testing Success!")
    else:
        for v in sut.get_racks():
            print(v.rack_name)
            print(str(v.__dict__))
    

