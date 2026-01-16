# Mission: Manage a folder of book archive files. Others soon.

# STATUS: Needs testing.

# License: MIT
import os, os.path, sys, time, shutil
from pathlib import Path

if '..' not in sys.path:
    sys.path.append('..')

from bible9000.sierra_dao  import SierraDAO
from bible9000.tui         import BasicTui
from bible9000.sierra_note import NoteDAO
from bible9000.sierra_fav  import FavDAO
from bible9000.ArchiveOne.arch_book import *

class BookArchiveManager:
    ''' Manage unary ArchBook files, only. '''
    def __init__(self, archive_folder=None):
        ''' Will always have an archive folder - yet other directories ok as well. '''
        self.__archive_folder = None
        self.__home = str(Path(__file__).parent.resolve())
        if not self.set_folder(archive_folder):
            self.__archive_folder = self.__home

    def set_folder(self, archive_folder)->bool:
        ''' Set the ArchiveManager location. Folder must exist. True on success.'''
        if archive_folder and os.path.exists(archive_folder):
            self.__archive_folder = archive_folder
            return True
        else:
            return False

    def list_archives(self)->list:
        ''' Show all archive files in the present location. Presently only book files. '''
        results = []
        for file in os.listdir(self.__archive_folder):
            if file.endswith(ArchBook.FILE_TYPE):
                results.append(os.path.sep.join(self.__archive_folder, file))
        return sorted(results)

    def import_archive(self, archive_file)->bool:
        ''' Import a book definition to the library.'''
        if not ArchBook.IsBookArchive(archive_file):
            return False
        try:
            shutil.copy(archive_file, self.__archive_folder)
        except:
            return False
        return True

    def export_archive(self, fq_archive_file, destination_folder)->bool:
        ''' Copy a fully-qualified book archive elsewhere. '''
        if not fq_archive_file in self.list_archives():
            return False
        copy = BookArchiveManager(destination_folder) # meh
        return copy.import_archive(fq_archive_file)

    def delete_archive(self, fq_archive_file)->bool:
        ''' Destroy a fully-qualified book archive file. '''
        if not fq_archive_file in self.list_archives():
            return False
        os.unlink(fq_archive_file)
        return not os.path.exists(fq_archive_file)


def do_library_admin_help(**kwargs):
    BasicTui.Display('?: [Help] to show this menu.')
    BasicTui.Display('q: [Return] to previous session.')
    BasicTui.Display('~~~~~')


def do_library_ops(**kwargs):
    from bible9000.main import do_func, dum
    ''' What users can do. '''
    options = [
        ("?", "Help", do_library_admin_help),
        ("q", "Quit", dum)
    ]
    do_func("Librarian: ", options, '>> Book Menu', **kwargs)        


if __name__ == '__main__':
    do_library_ops() # default db ok!

