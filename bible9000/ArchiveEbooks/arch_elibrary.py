# Mission: Manage the ebook library.
import sys
if '..' not in sys.path:
    sys.path.append('..')

import os, sqlite3, zipfile
from pathlib import Path


''' 
Metaphore is:

ArchVerse   0..*:1 ArchBook
ArchBook       1:1 ArchEbook
ArchEbook   0..*:1 ArchElibrary

And everything has a version.
'''
from ArchiveOne.arch_verse import *
from ArchiveOne.arch_book import *
from ArchiveEbooks.arch_ebook import *

class ArchElibrary(ArchVersion):
    
    def __init__(self, ver:float=0, short_name:str='', desc:str='', code=0):
        super().__init__(ver, short_name, desc, code)
        home = str(Path(__file__).resolve().parent)
        self.__info = os.sep.join((home, 'ebooks.info'))
        self.__db   = os.sep.join((home, 'ebooks.info.sqlt3'))
        self.__zip  = os.sep.join((home, 'ebooks.info.zip'))

    def connect_db(self, fq_file):
        conn = sqlite3.connect(fq_file)
        conn.row_factory = sqlite3.Row
        return conn

    def search_catalog(self, fq_file, title_query):
        with self.connect_db(fq_file) as conn:
            cursor = conn.cursor()
            # Use LIKE for partial matches in title
            cursor.execute("SELECT * FROM book_meta WHERE book_title LIKE ?", (f'%{title_query}%',))
            return cursor.fetchall()


    def update_status(self, fq_file, book_id, new_status):
        with self.connect_db(fq_file) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE book_meta SET status = ? WHERE id = ?", (new_status, book_id))
            conn.commit()

    def title_match(self, word):
        results = []
        if not self.exists_db():
            return results
        for match in self.search_catalog(self.__db, word):
            results.append(ArchEbook.Clone(dict(match)))
        return results

    def exists_db(self):
        ''' See if the data-file exists '''
        try:
            return os.path.exists(self.__db)
        except:
            return False
               
    def exists_zip(self):
        ''' See if the zip-file exists & is valid '''
        try:
            if os.path.exists(self.__zip):
                return zipfile.is_zipfile(self.__zip)
        except:
            return False

    def setup(self)->tuple:
        import shutil
        if not self.exists_zip():
            return False, f"Unable to stat '{self.__zip}'."
        shutil.unpack_archive(self.__zip)
        if not self.exists_db():
            return False, f"Unable to unpack '{self.__zip}'."
        return True, "ToDo"

    def find_books(self):
        pass



if __name__ == '__main__':
    sut = ArchElibrary(0.1, 'basic link', 'Potential')
    print(sut.setup())
    if not sut.exists_db(): # and sut.exists_info():
        print("Error 10010.")
        exit(10010)
    for line in sut.title_match('mormon'):
        print(line.link)
        
    print("Testing Success.")
    

