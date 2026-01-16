import sys
if '..' not in sys.path:
    sys.path.append('..')

''' 
Metaphore is simple:

ArchVerse   *:1 ArchBook
ArchBook    *:1 ArchShelf
ArchShelf   *:1 ArchStack
ArchLibrary *:1 Arch Stack

And everything has a version.
'''
class ArchVersion:
    ''' Safe coding is no accident ... ;^) '''    
    def __init__(self, ver:float=0, short_name:str='', desc:str='', code=0):
        self.version = ver
        self.name = short_name
        self.description = desc
        self.code = code
        self.author = list()
        self.copyright = ''

    def __str__(self):
        import json
        return json.dumps(self.__dict__)


class ArchVerse:
    ''' Verses in any archive need books names, please. '''
    def __init__(self):
        self.sierra_num = 0
        self.book_name = ''
        self.chapter_num = 0
        self.verse_num = 0
        self.text = '' # typically a sentance / fragment, but can be a full verse.

    def __str__(self):
        import json
        return json.dumps(self.__dict__)

    def get_verse(self):
        return dict(self.__dict__) # here's your copy ;^)

    @staticmethod
    def Clone(obj):
        ''' Returns an instance if it gets one, else None. '''
        result = None
        if isinstance(obj, ArchVerse):
            result = ArchVerse()
            result.__dict__ = dict(obj.__dict__) # clone it
        elif isinstance(obj, dict):
            result = ArchVerse()
            if set(obj) != set(result.__dict__):
                return None
            result.__dict__ = dict(obj) # clone it
        return result

if __name__ == '__main__':
    a = ArchVerse()
    a.sierra_num = 99
    a.book_name = 'Test Booker.'
    a.chapter_num = 9
    a.verse_num = 8
    a.text = '# typically a sentance / fragment, but can be a full verse.'
    c = ArchVerse.Clone(a)
    if not c:
        print("Error 0001.")
    if id(c) == id(a):
        print("Error 0002.")
    c = ArchVerse.Clone(c.__dict__)
    if not c:
        print("Error 0003.")
    if id(c) == id(a):
        print("Error 0004.")
    if c.__dict__ != a.__dict__:
        print("Error 0010: Bad clone.")
    else:
        print("Testing Success!")
