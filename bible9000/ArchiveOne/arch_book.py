''' 
Metaphore is simple:

ArchVerse   *:1 ArchBook
ArchBook    *:1 ArchShelf
ArchShelf   *:1 ArchStack
ArchLibrary *:1 Arch Stack

And everything has a version.
'''
from arch_verse import *

class ArchBook(ArchVersion):
    
    def __init__(self, ver:float=0.0, short_name:str='', desc:str='', code=0):
        super().__init__(ver, short_name, desc, code)
        self.__verses = list()

    def get_verses(self):
        return list(self.__verses) # mod the verses, not my list.

    def append_verse(self, a_verse)->int:
        ''' The verse should be and instace of ArchiveVerse, please. '''
        if not isinstance(a_verse, ArchVerse):
            return -1
        self.__verses.append(ArchVerse.Clone(a_verse)) # precious
        return len(self.__verses)

    def remove_verse(self, verse_num):
        ''' Remove a ones-based verse identifier from the list. '''
        if verse_num < 1 or verse_num > len(self.__verses):
            return None
        return self.__verses.pop(verse_num - 1)

    @staticmethod
    def Clone(obj):
        ''' Returns an instance if it gets one, else None. '''
        result = None
        if isinstance(obj, ArchBook):
            result = ArchBook()
            result.__dict__ = dict(obj.__dict__) # clone it
        elif isinstance(obj, dict):
            result = ArchBook()
            if set(obj) != set(result.__dict__):
                return None
            result.__dict__ = dict(obj) # clone it
        return result


if __name__ == '__main__':
    sut = ArchBook(0.1, 'basic book', 'Just passin thru'); test_case = 10
    for i in range(test_case):
        a = ArchVerse()
        a.book_name = 'Book ' + str(i)
        a.chapter_num = i
        a.verse_num = i
        a.text = 'Verse ' + str(i)
        if sut.append_verse(a) != len(sut.get_verses()):
            print("Error 1000.")
            break
    
    if not len(sut.get_verses()) == test_case:
        print("Error 1010.")
    for _ in range(test_case):
        goober = sut.remove_verse(1)
        del goober
    if len(sut.get_verses()) == 0:
        print("Testing Success!")
    else:
        for v in sut.get_verses():
            print(v.book_name)
            print(str(v.__dict__))
    

