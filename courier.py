# coding:utf-8  
import os  
import sys
import importlib
importlib.reload(sys)
import MySQLdb
import importlib
import dealwithdb as deal

class Courier():
    def __init__(self, name, password, cinemaID):
        self.name = name
        self.password = password

def getnamelist():
    db, cursor = deal.connect2db()
    sql = "SELECT name FROM Courier"
    cursor.execute(sql)
    db.commit()
    deliverylist = cursor.fetchall()
    return deliverylist


if __name__ == "__main__":
    pass