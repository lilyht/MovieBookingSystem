# coding:utf-8  
import os  
import sys
import dealwithdb as deal
import importlib
importlib.reload(sys)
import MySQLdb
import importlib

class Morder():
    def __init__(self, orderID, movie='', cinemaID='', seatrank='', seatnum='', phone='', addr='', 
                    isFinished=0, cost=0, tansactiontime='', courier=''):
        self.orderID = orderID
        self.movie = movie
        self.cinemaID = cinemaID
        self.seatrank = seatrank
        self.seatnum = seatnum
        self.phone = phone
        self.addr = addr
        self.isFinished = isFinished
        self.cost = cost
        self.tansactiontime = tansactiontime
        self.courier = courier
        print('初始化')
    
    def insertmorder(self):
        msg = ''
        db, cursor = deal.connect2db()
        sql = "INSERT into MOrder values ('{}', '{}', {}, '{}', '{}', '{}', '{}', {}, {}, '{}', '{}');".format(\
            self.orderID, self.movie, int(self.cinemaID), self.seatrank, self.seatnum, self.phone, self.addr, 0,
             self.cost, self.tansactiontime, self.courier)
        print(sql)
        cursor.execute(sql)
        db.commit()
        msg = 'order'
        return msg

def count():
    db, cursor = deal.connect2db()
    sql = "SELECT count(*) from MOrder"
    cursor.execute(sql)
    db.commit()
    ordernum = cursor.fetchone()  # 总订单数
    return ordernum
    
def getorder(cinemaID):
    db, cursor = deal.connect2db()
    sql = "SELECT * FROM MOrder WHERE courier = '' AND cinemaID = {}".format(cinemaID)
    cursor.execute(sql)
    db.commit()
    res = cursor.fetchall()
    reslen = len(res)
    if reslen == 0:
        msg = "empty"
    else:
        msg = "have"
    return msg, res

def finished(morderID):
    db, cursor = deal.connect2db()
    sql = "UPDATE MOrder set isFinished = 1 WHERE orderID = '{}'".format(morderID)
    cursor.execute(sql)
    db.commit()

def delete(morderID):
    db, cursor = deal.connect2db()
    sql = "DELETE FROM MOrder WHERE orderID = '{}' ".format(morderID)
    cursor.execute(sql)
    db.commit()