import os
import sys
import sqlite3
import time
import hashlib

"""Ritorna il percorso del database"""
def getdbname():
    return os.path.splitext(os.path.basename(__file__))[0] + '.db'

"""Si connette al db SQLite"""
def connectdb():
    try:
        dbfile = getdbname()
        conn = sqlite3.connect(dbfile, timeout=2)
        return conn
    except:
        print("Qualcosa è andato storto")

"""Funzione che esegue query senza connessione alla base"""
def runcmdnoconn(query, args=None):
    result = False
    try:
        conn = connectdb()
        if not conn is None:
            result = runcmd(conn,query,args)
        conn.close()
    except:
        print("errore in runcmdnoconn")
    return result

"""Funzione base che esegue query senza risultato"""
def runcmd(conn, query, args=None):
    args = args or []
    result = False
    try:
        cursor = conn.execute(query, args)
        conn.commit()
        cursor.close()
        result = True
    except Exception as err:
        print("errore in esecuzione query")
        print(err)
    return result

"""Esiste la tabella?"""
def tableexists(table):
    result = False
    try:
        conn = connectdb()
        if not conn is None:
            query = "SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?"
            args = (table,)
            cur = conn.execute(query, args)
            item = cur.fetchone()
            result = not item is None
            cur.close()
            conn.close()
    except:
        print ("tableexist ERROR")
    return result

"""Crea tabella"""
def createhashtable():
    if tableexists('files'):
        return True
    query = "CREATE TABLE files (id INTEGER PRIMARY KEY, fname VARCHAR(255) NOT NULL, md5 BLOB NOT NULL)"
    return runcmdnoconn(query)

"""Crea indice"""
def createhashtableidx():
    if tableexists('files'):
        query = 'CREATE INDEX IF NOT EXISTS idxfile ON files (fname)'
        return runcmdnoconn(query)
    return False

"""Update the SQLite File Table"""
def updatehashtable(fname, md5):
    qry = "UPDATE files SET md5 = ? WHERE fname = ?"
    return runcmdnoconn(qry,(md5,fname))

"""Insert into the SQLite File Table"""
def inserthashtable(fname, md5):
    qry = "INSERT INTO files (fname, md5) VALUES (?,?)" 
    return runcmdnoconn(qry, (fname, md5))

"""Setup's the Hash Table"""
def setuphashtable():
   createhashtable()
   createhashtableidx()

"""Checks if md5 hash tag exists in the SQLite DB"""
def md5indb(fname):
    items = []
    if tableexists('files'):
        try:
            conn = connectdb()
            if not conn is None:
                qry = "SELECT md5 FROM files WHERE fname = ?"
                try:
                    cursor = conn.execute(qry,(fname,))
                    for item in cursor:
                        items.append(item[0])
                except Exception as ex:
                    print(ex)
        except:
            pass
    return items

def haschanged(fname, md5):
    items = md5indb(fname)
    if items.__contains__(md5):
        pass


def getfileext(fname):
    """Get the file name extension"""
    return os.path.splitext(fname)[1]

def getmoddate(fname):
    """Get file modified date"""
    try:
        mtime = os.path.getmtime(fname)
        mtime = time.ctime(mtime)
    return mtime

def md5short(fname):
    """Get md5 file hash tag"""
    with open(fname, 'rb', 'utf-8') as openfile:
        content = openfile.read()
        result = hashlib.md5(content).digest()
    return result

"""Test"""
if __name__ == "__main__":
    try:
        setuphashtable()
        print(inserthashtable('test', bytearray([1,2,3,4,5])))
        print(md5indb("test"))
        print(updatehashtable('test', bytearray([1,2,3,4,6])))
        print(md5indb("test"))

    except:
        print("Nulla da dichiarare")
