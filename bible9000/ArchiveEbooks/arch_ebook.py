import sys
if '..' not in sys.path:
    sys.path.append('..')

''' 
Metaphore is:

ArchVerse   0..*:1 ArchBook
ArchBook       1:1 ArchEbook
ArchEbook   0..*:1 ArchELibrary

And everything has a version.
'''
from ArchiveOne.arch_verse import *
from ArchiveOne.arch_book import *

class ArchEbook(ArchVersion):
    
    def __init__(self, ver:float=0, short_name:str='', desc:str='', code=0):
        super().__init__(ver, short_name, desc, code)
        self.id          = 0
        self.book_type   = ''
        self.dated       = ''
        self.sierra      = 0
        self.book_title  = ''
        self.language    = ''
        self.authors     = ''
        self.subjects    = ''
        self.lib_cong    = ''
        self.shelves     = ''        
        self.link        = ''
        self.code        = 0


    @staticmethod
    def Clone(obj):
        ''' Returns an instance if it gets one, else None. '''
        result = None
        if isinstance(obj, ArchEbook):
            result = ArchEbook()
            result.__dict__ = dict(obj.__dict__) # clone it
        elif isinstance(obj, dict):
            result = ArchEbook()
            result.id           = obj['id']
            result.book_type    = obj['BOOK_TYPE']
            result.dated        = obj['DATED']
            result.sierra       = obj['book_number']
            result.book_title   = obj['book_title']
            result.language     = obj['language']
            result.authors      = obj['AUTHORS']
            result.subjects     = obj['SUBJECTS']
            result.lib_cong     = obj['LoCC']
            result.shelves      = obj['SHELVES']         
            result.link         = obj['LINK']
            result.code         = obj['STATUS']
        return result


if __name__ == '__main__':
    sut = ArchEbook(0.1, 'basic rack', 'Just passin thru'); test_case = 10
    

