#!/usr/bin/env python3
# License: MIT
'''
File: tests.py
Problem Domain: Regression testing
Status: Testing Success
Revision: 2.0.0
'''

import io,sys
if '..' not in sys.path:
    sys.path.append('..')
    
from contextlib import redirect_stdout
from bible9000.tui import BasicTui
from bible9000.sierra_dao import SierraDAO
from bible9000.sierra_note import NoteDAO
from bible9000.words import WordList
from bible9000.sierra_fav import FavDAO
from bible9000.fast_path import FastPath

def test_dao(**kwargs):
    ''' Ye Olde Testing '''
    rows = SierraDAO.ListBooks(**kwargs)
    if len(list(rows)) != 81:
        BasicTui.DisplayError("Testing Failure - No Books?")
        quit()

    dao = SierraDAO.GetDAO(**kwargs)
    rows = dao.search("verse LIKE '%PERFECT%'")
    if len(list(rows)) < 124:
        BasicTui.DisplayError("Testing Failure")
    else:
        BasicTui.Display("Testing Success")

def test_favs(**kwargs):
    import os, os.path
    testdb = kwargs['db']
    if os.path.exists(testdb):
        os.unlink(testdb)
    if os.path.exists(testdb):
        raise Exception(f'Unable to remove "{testdb}"?')
    from bible9000.admin_ops import tables
    db = FavDAO.GetDAO(**kwargs)
    db.dao.conn.execute(tables['SqlFav'])
    tests = [
        1, 2, 12, 3000, 3100
        ]

    for t in tests:
        db.toggle_fav(t)        
    for row in db.get_favs():
        if not db.is_fav(row):
            raise Exception("is_fav: - error")

    for t in tests:
        db.toggle_fav(t)
        if db.is_fav(t):
            raise Exception("is_fav: + error")
    for row in db.get_favs():
        print(row)
    # db.dao.conn.connection.rollback()
    db.dao.conn.connection.close()
    if os.path.exists(testdb):
        os.unlink(testdb)

def test_words():
    lines = WordList.Edit(None)
    lines = WordList.Edit('')
    zin = 'able.|$"baker".|$charley.|$delta.|$zulu'
    lines = WordList.Edit(zin)
    print(lines)


def test_notes(**kwargs):
    import os, os.path
    testdb = kwargs['db']
    if os.path.exists(testdb):
        os.unlink(testdb)
    if os.path.exists(testdb):
        raise Exception(f'Unable to remove "{testdb}"?')
    from bible9000.admin_ops import tables
    db = NoteDAO.GetDAO(**kwargs)
    db.dao.conn.execute(tables['SqlNotes'])
    tests = [
        1, 2, 12, 3000, 3100
        ]
    for t in tests:
        row = NoteDAO(**kwargs)
        row.vStart  = t
        row.Notes   = f"note{t}"
        row.Subject = f"subject{t}"
        db.insert_or_update_note(row)
    for row in list(db.get_all()):
        cols = row.Notes
        cols[0] = 'Updated ' + cols[0]
        row.Notes = cols
        cols = row.Subject
        if not cols:
            print(row)
            print("Error: row.Subject error.", file=sys.stderr)
        else:
            cols[0] = 'Updated ' + cols[0]
            row.Subject = cols
            db.update_note(row)
        print('~')
    for row in db.get_all():
        print('ZNOTE',row.__dict__)
    print('SLISTS',db.get_subjects_list())
    # db.dao.conn.connection.rollback()
    db.dao.conn.connection.close()
    if os.path.exists(testdb):
        os.unlink(testdb)

def test_nav():
    from main import mainloop
    ostdin  = sys.stdin
    ostdout = sys.stdout

    osession = io.StringIO()
    sys.stdout = osession
    
    isession = "v.1.1.q.q.q" # test reset :^)
    sys.stdin = io.StringIO(isession)

    # with redirect_stdout(output_buffer): # meh
    mainloop()
    FastPath.Reset()
    sys.stdin  = ostdin
    sys.stdout = ostdout
    print(osession.getvalue())


if __name__ == '__main__':
    test_nav()
    # test_dao() -> used official database... not used here, but by dao.
    test_words()
    test_notes(db="~test.sqlt3")
    test_favs(db="~test.sqlt3")
    BasicTui.Display("Testing Success")

