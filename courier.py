# coding:utf-8  
import os  
import sys
import importlib
importlib.reload(sys)
import MySQLdb
import importlib
import dealwithdb as deal

class Courier():
    def __init__(self, name, password, morderID='0'):
        self.name = name
        self.password = password
        self.morderID = morderID
    
    def CourierLogin(self):
        db, cursor = deal.connect2db()
        sql = "SELECT * from COURIER where name = '{}' and password='{}'".format(self.name, self.password)
        cursor.execute(sql)
        db.commit()
        res = cursor.fetchall()
        num = 0
        num = len(res)
        # 如果存在该电配送员且密码正确
        if num == 1:
            print("登录成功！欢迎配送员！")
            msg = "done3"
        else:
            print("您没有配送员权限或登录信息出错。")
            msg = "fail3"
        return msg

    def delivery(self, morderID, msg):
        db, cursor = deal.connect2db()
        if msg == 'done':
            sql = "UPDATE MOrder SET isFinished = 1 WHERE courier = {}".format(self.name)
        elif msg == 'fail':
            sql = "DELETE FROM MOrder WHERE morderID = {}".format(morderID)
        cursor.execute(sql)
        db.commit()


def getnamelist():
    db, cursor = deal.connect2db()
    sql = "SELECT name FROM Courier"
    cursor.execute(sql)
    db.commit()
    deliverylist = cursor.fetchall()
    return deliverylist

def getorderlist(couriername):
    db, cursor = deal.connect2db()
    sql = "SELECT * FROM morder WHERE isFinished = 0 AND courier = '{}'".format(couriername)
    print(sql)
    cursor.execute(sql)
    db.commit()
    orderlist = cursor.fetchall()
    if len(orderlist) == 0:
        msg = 'empty'
    else:
        msg = 'have'
    return msg, orderlist
    

if __name__ == "__main__":
    pass