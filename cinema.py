# coding:utf-8  
import os  
import sys
import dealwithdb as deal
import importlib
importlib.reload(sys)
import MySQLdb
import importlib

class Cinema():
    def __init__(self, cinemaID, cname='', caddr='', cphone='', imagesrc='', acapacity=0, bcapacity=0):
        self.cinemaID = cinemaID
        self.cname = cname
        self.caddr = caddr
        self.cphone = cphone
        self.imagesrc = imagesrc
        self.acapacity = acapacity
        self.bcapacity = bcapacity
    
    def insertcinema(self):
        msg = ''
        db, cursor = deal.connect2db()
        sql = "INSERT INTO Cinema VALUES ({}, '{}', '{}', '{}', '{}', {}, {})".format(\
                self.cinemaID, self.cname, self.caddr, self.cphone, self.imagesrc, self.acapacity, self.bcapacity)
        cursor.execute(sql)
        db.commit()
        msg = 'done'
        return msg
    
    def getinfo(self):
        db, cursor = deal.connect2db()
        sql = "SELECT * from Cinema WHERE cinemaID = {}".format(self.cinemaID)
        cursor.execute(sql)
        db.commit()
        cininfo = cursor.fetchone()
        return cininfo
    

def getcinemanum():
    db, cursor = deal.connect2db()
    sql1 = "SELECT MAX(cinemaID) from Cinema"
    cursor.execute(sql1)
    db.commit()
    cnum = cursor.fetchone()  # 总影院数
    return cnum

def waitforassign():
    db, cursor = deal.connect2db()
    # 查询待分配电影院
    sql = ('select C.cinemaID, C.cname from cinema C WHERE C.cinemaID not in '
        '(select distinct CA.cinemaID from CinAdmin CA WHERE CA.cinemaID is not NULL);')
    print(sql)
    cursor.execute(sql)
    db.commit()
    res = cursor.fetchall()
    reslen = len(res)
    return res, reslen

def updatecinema(cname, caddr, cphone, acapacity, bcapacity):
    db, cursor = deal.connect2db()
    sql = "UPDATE Cinema SET caddr='{}', cphone='{}', acapacity={}, bcapacity={} WHERE cname = '{}'".format(caddr, cphone, acapacity, bcapacity, cname)
    cursor.execute(sql)
    db.commit()