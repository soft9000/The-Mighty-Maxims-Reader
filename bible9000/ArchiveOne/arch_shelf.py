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
from ArchiveOne.arch_book import *

class ArchShelf(ArchVersion):
    
    def __init__(self, ver:float=0, short_name:str='', desc:str='', code=0):
        super().__init__(ver, short_name, desc, code)
        self.__books = list()

    def get_books(self):
        return list(self.__books) # mod the books, not my list.

    def append_book(self, a_book)->int:
        ''' The book should be and instace of Archivebook, please. '''
        if not isinstance(a_book, ArchBook):
            return -1
        self.__books.append(ArchBook.Clone(a_book)) # precious
        return len(self.__books)

    def remove_book(self, book_num):
        ''' Remove a ones-based book identifier from the list. '''
        if book_num < 1 or book_num > len(self.__books):
            return None
        return self.__books.pop(book_num - 1)

    @staticmethod
    def Clone(obj):
        ''' Returns an instance if it gets one, else None. '''
        result = None
        if isinstance(obj, ArchShelf):
            result = ArchShelf()
            result.__dict__ = dict(obj.__dict__) # clone it
        elif isinstance(obj, dict):
            result = ArchShelf()
            if set(obj) != set(result.__dict__):
                return None
            result.__dict__ = dict(obj) # clone it
        return result


if __name__ == '__main__':
    sut = ArchShelf(0.1, 'basic shelf', 'Just passin thru'); test_case = 10
    for i in range(test_case):
        a = ArchBook(0.1, 'basic book', '''Just bookin' thru''')
        if sut.append_book(a) != len(sut.get_books()):
            print("Error 1000.")
            break
    
    if not len(sut.get_books()) == test_case:
        print("Error 1010.")
    for _ in range(test_case):
        goober = sut.remove_book(1)
        del goober
    if len(sut.get_books()) == 0:
        print("Testing Success!")
    else:
        for v in sut.get_books():
            print(v.book_name)
            print(str(v.__dict__))
    

