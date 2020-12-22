import os
import sys
import sqlite3

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


"""Test"""
if __name__ == "__main__":
    try:
        cnn = connectdb()
        cnn.close()
    except:
        print("Nulla da dichiarare")
