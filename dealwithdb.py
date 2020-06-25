# coding:utf-8  
import os  
import sys
import importlib
importlib.reload(sys)
import MySQLdb
import importlib

def connect2db():
    db = MySQLdb.connect("localhost", "root", "", "MBDB", charset='utf8')
    cursor = db.cursor()
    try:
        cursor.execute("use MBDB")
    except:
        print("Error: unable to use database!")
    return db, cursor

if __name__ == "__main__":
    pass