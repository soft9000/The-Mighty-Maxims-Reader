#!/usr/bin/env python3
'''
License: MIT
File: main.py
Problem Domain: Console Application
'''

STATUS   = "TESTING"
VERSION  = "2.5.0"
MAX_FIND = 40 # When to enter 'tally only' mode

'''
MISSION
=======
Create a simple way to read & collect your favorite passages
using every operating system where Python is available.

NEXUS
----- 
Installer: https://pypi.org/project/Bible9000/
Project:   https://github.com/DoctorQuote/The-Stick-of-Joseph
Website:   https://mightymaxims.com/
'''

import sys
if '..' not in sys.path:
    sys.path.append('..')

from bible9000.sierra_dao  import SierraDAO
from bible9000.sierra_note import NoteDAO
from bible9000.sierra_fav  import FavDAO
from bible9000.tui import BasicTui
from bible9000.words import WordList
from bible9000.fast_path import FastPath
from bible9000.report_html import export_notes_to_html
from bible9000.user_selects import UserSelects
from bible9000.admin_ops import *


def dum(**kwargs):
    BasicTui.Display('(done)')


def do_func(prompt, options, level, **kwargs):
    '''Menued operations. '''
    choice = None
    while choice != options[-1][0]:
        if level:
            BasicTui.DisplayTitle(level)
        for o in options:
            BasicTui.Display(o[0], o[1])
        choice = BasicTui.Input(prompt)
        if not choice:
            continue
        choice = choice[0].lower()
        BasicTui.Display(f">> {choice}")
        for o in options:
            if o[0] == choice:
                BasicTui.DisplayTitle(o[1])
                o[2](**kwargs)


def do_search_subjects(**kwargs):
    ''' Mass-manage all subjects. '''
    dao = NoteDAO.GetDAO(**kwargs)
    while True:
        subjects = dao.get_subjects_list()
        ss = 0; subject = None
        for ss, subject in enumerate(subjects,1):
            BasicTui.Display(f'{ss}.) {subject}')
        BasicTui.Display(f"Found {ss} Subjects.")
        if not ss:
            return
        which = BasicTui.InputNumber("Number: ")
        if which < 1 or which > len(subjects):
            BasicTui.DisplayError('Selection out of range.')
            return
        subject = subjects[which - 1]
        option = BasicTui.InputOnly('?','r', 'd', 'q')
        if not option: return
        if option[0] == '?':
            BasicTui.Display('? = Help (show this :-)')
            BasicTui.Display('r = Rename Subject')       
            BasicTui.Display('d = Delete Subject')
            BasicTui.Display('q = Return to previous')
            continue
        if option[0] == 'd':
            b = dao.subject_delete(subject, **kwargs)
            if b:
                BasicTui.Display(f"Removed Subject '{subject}'")
            else:
                BasicTui.DisplayError(f"Error: Subject '{subject}' not deleted.")
            continue
        if option[0] == 'r':
            nname = BasicTui.Input(f'Rename "{subject}" to: ')
            b = dao.subject_rename(subject, nname, **kwargs)
            if b:
                BasicTui.Display(f"Renamed Subject '{subject}'")
            else:
                BasicTui.DisplayError(f"Error: Subject '{subject}' not deleted.")
            continue
        return None


def do_search_books(**kwargs):
    ''' Search books & read from results. '''
    while True:
        yikes = False # search overflow
        BasicTui.Display("Example: +word -word, -a")
        BasicTui.Display("Enter q to quit")
        inc = ''; count = 0; exbook = {}
        words = BasicTui.InputOnly("?", "+w", "-w", "q")
        cols = words.strip().split(' ')
        for word in cols:
            if not word or word == 'q':
                return
            if word == '?':
                BasicTui.DisplayHelp("?  = help",
                    "+w = include word",
                    "-w = exclude word")
                break
            if inc:
                inc += ' AND '
            if word[0] == '-':
                inc += f'VERSE NOT LIKE "%{word[1:]}%"'
                count += 1
            if word[0] == '+':
                inc += f'VERSE LIKE "%{word[1:]}%"'
                count += 1
        if not count:
            continue
        dao = SierraDAO.GetDAO(**kwargs)
        sigma = 0
        for row in dao.search(inc):
            if exbook:
                _id = row['book']
            sigma += 1
            if sigma == MAX_FIND:
                yikes = True
                BasicTui.DisplayError(f"Results >= {MAX_FIND} ...")
            if not yikes:
                BasicTui.DisplayVerse(row, **kwargs)
        if exbook:
            BasicTui.DisplayTitle("Omissions")
            for key in exbook:
                BasicTui.Display(f'{key} has {exbook[key]} matches.')
        BasicTui.DisplayTitle(f"Detected {sigma} Verses")


def do_list_books(**kwargs):
    ''' Displays the books. Returns number of books displayed
        to permit selections of same.
    '''
    return BasicTui.DisplayBooks(**kwargs)


def do_random_reader(**kwargs)->int:
    ''' Start reading at a random location.
        Return the last Sierra number shown.
    '''
    dao = SierraDAO.GetDAO(**kwargs)
    res = dao.conn.execute('SELECT COUNT(*) FROM SqlTblVerse;')
    vmax = res.fetchone()[0]+1
    import random    
    sierra = random.randrange(1,vmax)
    return browse_from(sierra, **kwargs)


def do_sierra_reader(**kwargs)->int:
    ''' Start reading at a Sierra location.
        Return the last Sierra number shown.
        Zero on error.
    '''
    books = []
    for row in SierraDAO.ListBooks(**kwargs):
        books.append(row['book'].lower())
    last_book = do_list_books(**kwargs)
    inum = BasicTui.InputNumber('Book # > ')
    if inum > 0 and inum <= last_book:
        ubook = books[inum-1]
        BasicTui.Display(f'Got {ubook}.')
        vrange = SierraDAO.GetBookRange(inum)
        vnum = BasicTui.InputNumber(f'Book numbers {vrange} > ')
        return browse_from(vnum, **kwargs)               
    else:
        return 0


def do_classic_reader(**kwargs):
    ''' Start browsing by classic chapter:verse. '''
    BasicTui.DisplayBooks()
    ibook = BasicTui.InputNumber("Book #> ")
    if ibook == -1:
        BasicTui.DisplayError("Bad book number.")
        return
    ichapt = BasicTui.InputNumber("Chapter #> ")
    if ichapt == -1:
        BasicTui.DisplayError("Bad chapter number.")
        return
    iverse = BasicTui.InputNumber("Verse #> ")
    if iverse == -1:
        BasicTui.DisplayError("Bad verse number.")
        return
    dao = SierraDAO.GetDAO(**kwargs)
    for res in dao.search(f'BookID = {ibook} AND BookChapterID = {ichapt} AND BookVerseID = {iverse}'):
        browse_from(dict(res)['sierra'], **kwargs)


def edit_notes(sierra, is_subject=False, **kwargs)->bool:
    ''' Manage the '.edit.' mode for any Sierra verse #. '''
    noun = 'Note'
    if is_subject:
        noun = 'Subject'
    sierra = int(sierra)
    dao = NoteDAO.GetDAO(**kwargs)
    row = dao.note_for(sierra)
    if not row: return False
    notes = []
    data = row.Notes
    if is_subject:
        data = row.Subject
    for ss, n in enumerate(data,1):
        line = f'{ss}.) {n}'
        BasicTui.Display(line)
        notes.append(n)

    inum = BasicTui.InputNumber("Number to edit > ") - 1
    if inum < 0:
        return False
    znote = BasicTui.Input(f'{noun}: ')
    if not znote:
        ok = BasicTui.InputYesNo(f'Delete {noun} (N/y) ?')
        if ok and ok.lower()[0] == 'y':
            notes.pop(inum)
        else:
            return False
    else:
        notes[inum] = znote # edited
    if is_subject:
        row.Subject = notes
    else:
        row.Notes = notes
    if row.is_null():
        dao.delete_note(row)
    else:
        dao.update_note(row)
        
    BasicTui.Display(f'{noun} updated.')
    BasicTui.Display('done')
    return True


def manage_notes(sierra, is_subject, **kwargs):
    ''' Create, edit, and delete notes for any Sierra verse #. '''
    noun = 'Note'
    if is_subject:
        noun = 'Subject'
    sierra = int(sierra)
    BasicTui.Display(f"Use .edit. to fix {noun}s")
    notes = BasicTui.Input(f'{noun}s: ')
    if not notes:
        BasicTui.Display(f"No {noun}.")
        return
    if notes == '.edit.':
        return edit_notes(sierra, is_subject, **kwargs)
    dao = NoteDAO.GetDAO(**kwargs)
    row = dao.note_for(sierra)
    if not row:
        row = NoteDAO()
    row.vStart = sierra
    if is_subject:
        row.add_subject(notes)
    else:
        row.add_note(notes)
    dao.insert_or_update_note(row)
    BasicTui.Display(f"{noun} added for {sierra}.")
    return True


def __edit_subjects(sierra, **kwargs): #unloced?
    ''' Associate 'subjects' with a Sierra verse.
        Subjects permit common 'topic threads' across
        a series of notes / stars. '''
    return edit_subjects(sierra, True, **kwargs)


def manage_subjects(sierra, **kwargs):
    ''' Create, edit, and delete subjects for any Sierra verse #. '''
    return manage_notes(sierra, True, **kwargs)

    
def browse_from(sierra, **kwargs)->int:
    ''' Start reading at a Sierra location.
        Return the last Sierra number shown.
        Zero on error.
    '''
    sierra = int(sierra)
    dao = SierraDAO.GetDAO(**kwargs)
    res = dao.conn.execute('SELECT COUNT(*) FROM SqlTblVerse;')
    vmax = res.fetchone()[0]+1
    
    verse = dict(*dao.search_verse(sierra))
    option = ''
    while option != 'q':
        if not BasicTui.DisplayVerse(verse, **kwargs):
            return 0
        # mainloop too much for a reader, methinks.
        option = BasicTui.InputOnly('?', '*', '@', '=', 'n', 'p', 'q')
        if not option:
            option = 'n'
        try:
            o = option[0]
            if o == '?':
                BasicTui.DisplayHelp('? = help',
                '* = toggle star',
                '@ = manage notes',
                '= = manage subjects',
                'n = next page',
                'p = last page',
                'q = quit')
                continue
            if o == '*':
                BasicTui.DisplayTitle('STAR')
                fdao = FavDAO.GetDAO(**kwargs)
                fdao.toggle_fav(sierra)
                if fdao.is_fav(sierra):
                    BasicTui.Display(f'Starred {sierra}!')
                else:
                    BasicTui.Display(f'De-starred {sierra}.')
                continue
            if o == '@':
                BasicTui.DisplayTitle('NOTES')
                manage_notes(sierra, False, **kwargs)
                continue
            if o == '=':
                BasicTui.DisplayTitle('SUBJECTS')
                manage_subjects(sierra, **kwargs)
                continue
            elif o == 'p':
                if sierra == 1:
                    BasicTui.Display('At the top.')
                    continue
                sierra -= 1
                verse = dict(*dao.search_verse(sierra))
            elif o == 'q':
                return sierra
            else: # default is 'n'
                if sierra == vmax:
                    BasicTui.Display('At the end.')
                    continue
                sierra += 1
                verse = dict(*dao.search_verse(sierra))
        except Exception as ex:
            BasicTui.DisplayError(ex)
            return sierra


def show_verse(sierra, **kwargs):
    dao = SierraDAO.GetDAO(**kwargs)
    verse = dict(*dao.search_verse(sierra))
    BasicTui.DisplayVerse(verse, **kwargs)    

 
def do_user_report(**kwargs):
    ''' Get all user notes & favs '''
    verses = UserSelects.GetSelections(**kwargs)
    for verse in verses:
        show_verse(verse, **kwargs)
    BasicTui.DisplayTitle(f'There are {len(verses)} Notes.')


def do_report_html(**kwargs):
    export_notes_to_html(**kwargs)


def do_help_do_notes_main():
    BasicTui.Display('s: [Search]')
    BasicTui.Display('Search all, either, or none to simply count words.')
    BasicTui.Display('~~~~~')
    BasicTui.Display('=: [Subjects]')
    BasicTui.Display('Display all subjects (pages) created so far.')
    BasicTui.Display('~~~~~')
    BasicTui.Display('#: [Report]')
    BasicTui.Display('Display the Note report.')
    BasicTui.Display('~~~~~')
    BasicTui.Display('$: [HTML Report]')
    BasicTui.Display('The HTML Report is a great way to share your \
notes, stars, and subjects with the rest of your world. Once exported \
your subject groups will combine the topics you feel can be \
presented together.')
    BasicTui.Display('~~~~~')
    BasicTui.Display('?: [Help]')
    BasicTui.Display('Show this list.')
    BasicTui.Display('~~~~~')
    BasicTui.Display('q: [Quit]')
    BasicTui.Display('Exit Notes.')
    BasicTui.Display('~~~~~')    


def do_notes_main(**kwargs):
    ''' Seaching & working with our notes. '''
    options = [
        ("s", "Search", do_search_books),
        ("=", "Subjects", do_search_subjects),
        ("@", "Display Notes", do_user_report),
        ("#", "Export HTML", do_report_html),
        ("?", "Help", do_help_do_notes_main),
        ("q", "Quit", dum)
        ]
    do_func("Option: ", options, '> Notes Menu', **kwargs)
    BasicTui.Display(".")
    

def do_help_main(**kwargs):
    ''' Explain the main options. '''
    BasicTui.Display('b: [List Books]')
    BasicTui.Display('List all book(s) in the database.')
    BasicTui.Display('~~~~~')
    BasicTui.Display('v: [ Sierra Reader]')
    BasicTui.Display('Select a book to start reading by verse number.')
    BasicTui.Display('~~~~~')
    BasicTui.Display('c: [Classic Reader]')
    BasicTui.Display("Select a book's number, chapter, and verse to start reading.")
    BasicTui.Display('~~~~~')
    BasicTui.Display('r: [Random Reader]')
    BasicTui.Display('See what fate might have you read today?')
    BasicTui.Display('~~~~~'),
    BasicTui.Display('n: [Report]'),
    BasicTui.Display('Notes & Searching.'),
    BasicTui.Display('~~~~~')
    BasicTui.Display('a: [Admin]')
    BasicTui.Display('Data import, export, and backup.')
    BasicTui.Display('~~~~~')
    BasicTui.Display('?: [Help]')
    BasicTui.Display('Show this list.')
    BasicTui.Display('~~~~~')
    BasicTui.Display('q: [Quit]')
    BasicTui.Display('Program exit.')
    BasicTui.Display('~~~~~')


def mainloop(**kwargs):
    ''' TUI features and functions. Use 'db'=sqlt3_file for alternate. '''
    options = [
        ("b", "List Books", do_list_books),
        ("v", "Sierra Reader", do_sierra_reader),
        ("c", "Classic Reader", do_classic_reader),
        ("r", "Random Reader", do_random_reader),
        ("n", "Notes", do_notes_main),
        ("a", "Admin", do_admin_ops),
        ("?", "Help", do_help_main),
        ("q", "Quit", dum)
    ]
    BasicTui.SetTitle('Mighty Maxims')
    BasicTui.Display(STATUS, 'Version', VERSION)
    do_func("Main Menu: ", options, '# Main Menu', **kwargs)
    BasicTui.Display(".")

    
if __name__ == '__main__':
    print('\n'*100)
    mainloop()
