import sys, os.path, json
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
from ArchiveOne.arch_verse import *


class ArchBook(ArchVersion):

    VERSIONS = [
        ArchVersion(1.0, 'ArchBook', 'Bible9000 Book Archive File', 20260115)
        ]

    FILE_TYPE = '.mmrb'
    
    def __init__(self, ver:float=0.0, short_name:str='', desc:str='', code=0):
        super().__init__(ver, short_name, desc, code)
        self.verses = list()

    def verse_count(self):
        return len(self.verses)

    def get_verses(self):
        return list(self.verses) # mod the verses, not my list.

    def get_verse(self, verse_num):
        try:
            return self.verses[verse_num]
        except:
            return None

    def append_verse(self, a_verse)->int:
        ''' The verse should be and instace of ArchiveVerse, please. '''
        if not isinstance(a_verse, ArchVerse):
            return -1
        self.verses.append(ArchVerse.Clone(a_verse)) # precious
        return len(self.verses)

    def remove_verse(self, verse_num):
        ''' Remove a ones-based verse identifier from the list. '''
        if verse_num < 1 or verse_num > len(self.verses):
            return None
        return self.verses.pop(verse_num - 1)

    def save_to(self, archive_file, overwrite=False)->tuple:
        ''' Save a book into a file. '''
        try:
            if not overwrite and os.path.exists(archive_file):
                return False, "Unable to overwrite existing file."
            with open(archive_file, 'w') as fh:
                info = dict()
                info['header'] = str(ArchBook.VERSIONS[0])
                meta = dict(self.__dict__)
                del meta['verses']
                info['meta']   = str(meta)
                print(json.dumps(info), file=fh)
                for v in self.verses:
                    print(str(v), file=fh)
        except Exception as ex:
            return False, str(ex)
        return True, "File saved."

    @staticmethod
    def CheckVersion(archive_file)->tuple:
        try:
            with open(archive_file) as fh:                
                info = eval(fh.readline())
                format_version = eval(info['header'])
                ver = format_version['version']
                bFound = False
                for v in ArchBook.VERSIONS:
                    if ver == v.version:
                        bFound = True
                        break
                if not bFound:
                    return False, f"Unable to read version {ver}."
                return True, "Archive file ok."
        except Exception as ex:
            return False, str(ex)
        
    @staticmethod
    def IsBookArchive(archive_file)->tuple:
        ''' Verify file exists and is a readable ArchBook. '''
        if not os.path.exists(archive_file):
            return False, "File not found"
        if not archive_file.endswith(ArchBook.FILE_TYPE):
            return False, "File name error"
        return ArchBook.CheckVersion(archive_file)

    @staticmethod
    def ReadFile(archive_file)->tuple:
        ''' Attempt to read an ArchBook from a file. '''
        stat = ArchBook.IsBookArchive(archive_file)
        if not stat[0]:
            return None, stat[1]
        try:
            result = ArchBook()
            with open(archive_file) as fh:                
                info = eval(fh.readline())
                format_version = eval(info['header'])
                ver = format_version['version']
                bFound = False
                for v in ArchBook.VERSIONS:
                    if ver == v.version:
                        bFound = True
                        break
                if not bFound:
                    return None, f"Unable to read version {ver}."
                meta = eval(info['meta'])
                result.version            = meta['version']
                result.name               = meta['name']
                result.description        = meta['description']
                result.code               = meta['code']
                result.author             = meta['author']
                result.copyright          = meta['copyright']
                for line in fh:
                    obj = eval(line)
                    verse = ArchVerse.Clone(obj)
                    result.append_verse(verse)
                return result, "Book archive loaded."
        except Exception as ex:
            return None, str(ex)
        return None, "Invalid operation." # safe coding is no accident.

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


def deep_comp(l, r)->tuple:
    for key in l.__dict__:
        if l.__dict__[key] != r.__dict__[key]:
            return False, f'Error: key "{key}" mismatch.'
    return True, "Testing Success"


def test_case():
    # STEP 1000: Basic test cases.
    sut = ArchBook(0.1, 'basic book', '1000 test cases'); test_case = 10
    for i in range(test_case):
        a = ArchVerse()
        a.book_name = 'Book ' + str(i)
        a.chapter_num = i
        a.verse_num = i
        a.text = 'Verse ' + str(i)
        if sut.append_verse(a) != len(sut.get_verses()):
            print("Error 1000.", file=sys.stderr)
            exit(1000)
    
    if not len(sut.get_verses()) == test_case:
        print("Error 1010.", file=sys.stderr)
        exit(1010)
    for _ in range(test_case):
        goober = sut.remove_verse(1)
        del goober
    if len(sut.get_verses()) != 0:
        for v in sut.get_verses():
            print(v.book_name, file=sys.stderr)
            print(str(v.__dict__), file=sys.stderr)
        exit(1011)
    # STEP 2000: I/O testing
    sut = ArchBook(0.1, 'basic book', '2000 test cases.')
    pattern = 'this is a test'.split()
    for v in pattern:
        av = ArchVerse()
        av.text = v
        sut.append_verse(av)
    if sut.verse_count() != len(pattern):
        print(f"Error 2010: Verse update error {sut.verse_count()}.", file=sys.stderr)
        exit(2010)
    TEST_FILE1 = './~One' + ArchBook.FILE_TYPE
    stat = sut.save_to(TEST_FILE1, True)
    if not stat[0]:
        print(f"Error 2020: {stat[1]}.", file=sys.stderr)
        exit(2020)
    stat = ArchBook.IsBookArchive(TEST_FILE1)
    if not stat[0]:
        print(f"Error 2030: [{stat[1]}].", file=sys.stderr)
        exit(2030)
    stat = ArchBook.ReadFile(TEST_FILE1)
    if not stat[0]:
        print(f"Error 2040: [{stat[1]}].", file=sys.stderr)
        exit(2040)
    imp = stat[0]
    if sut.verse_count() != imp.verse_count():
        print("Error 2050: Verse import error.", file=sys.stderr)
        exit(2050)
    # Destructive test
    del sut.__dict__['verses']; del imp.__dict__['verses']
    comp = deep_comp(sut,imp)
    if comp[0] == False:
        print(comp[1], file=sys.stderr)
        exit(2060)

    os.unlink(TEST_FILE1)
    print("Testing Success")



if __name__ == '__main__':
    test_case()
    

