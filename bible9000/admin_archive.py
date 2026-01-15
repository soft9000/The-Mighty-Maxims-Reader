# License: MIT
import os, os.path, sys, time
if '..' not in sys.path:
    sys.path.append('..')
from bible9000.sierra_dao import SierraDAO
from bible9000.tui        import BasicTui

from bible9000.sierra_note import NoteDAO
from bible9000.sierra_fav  import FavDAO

from bible9000.ArchiveOne import *


class ArchiveManager:
    def __init__(self, archive_folder = './'):
        self.archive_folder = archive_folder

    def set_folder(self, folder_name)->bool:
        pass

    def list_archives(self):
        ''' Show all archive files in the present location. '''
        pass

    def import_archive(self, archive_file)->bool:
        pass

    def export_archive(self, archive_file, destination_folder)->bool:
        pass

    def delete_archive(self, archive_file)->bool:
        pass


def do_library_admin_help():
    BasicTui.Display('q: [Return] to previous session.')
    BasicTui.Display('~~~~~')


def do_library_ops(**kwargs):
    from bible9000.main import do_func, dum
    ''' What users can do. '''
    options = [
        ("q", "Quit", dum)
    ]
    do_func("Librarian: ", options, '>> Library Menu', **kwargs)        


if __name__ == '__main__':
    do_library_ops() # default db ok!

