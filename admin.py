# coding:utf-8  
import os  
import sys
import importlib
importlib.reload(sys)
import MySQLdb
import importlib
import dealwithdb as deal

# 父类
class Admin():
    def __init__(self, adminname, password=''):
        self.adminname = adminname
        self.password = password

# 子类
class SysAdmin(Admin):
    def __init__(self, adminname, password):
        Admin.__init__(self, adminname, password)
    
    def SysAdminLogin(self):
        db, cursor = deal.connect2db()
        sql = "SELECT * from SYSADMIN where adminname = '{}' and password = '{}'".format(self.adminname, self.password)
        cursor.execute(sql)
        db.commit()
        res = cursor.fetchall()
        num = len(res)
        
        # 如果存在该管理员且密码正确
        if num == 1:
            print("登录成功！欢迎系统管理员！")
            msg = "done1"
        else:
            print("您没有系统管理员权限或登录信息出错。")
            msg = "fail1"
        return msg

# 子类
class CinAdmin(Admin):
    def __init__(self, adminname, password='', cinemaID=0):
        Admin.__init__(self, adminname, password)
        self.cinemaID = cinemaID

    def CinAdminLogin(self):
        db, cursor = deal.connect2db()
        sql = "SELECT * from CINADMIN where adminname = '{}' and password='{}'".format(self.adminname, self.password)
        cursor.execute(sql)
        db.commit()
        res = cursor.fetchall()
        num = 0
        num = len(res)
        # 如果存在该电影院管理员且密码正确
        if num == 1:
            print("登录成功！欢迎电影院管理员！")
            msg = "done2"
        else:
            print("您没有电影院管理员权限或登录信息出错。")
            msg = "fail2"
        return msg

    def assigncinadmin(self, cinemaID):
        db, cursor = deal.connect2db()
        # 分配电影院
        sql = "UPDATE CinAdmin SET cinemaID = {} WHERE adminname = '{}'".format(cinemaID, self.adminname)
        print(sql)
        cursor.execute(sql)
        db.commit()
        msg = 'done'
        return msg

    
    

def getavailablecin():
    # 查询空闲电影院管理员
    db, cursor = deal.connect2db()
    sql = "SELECT * from CinAdmin WHERE cinemaID is NULL"
    print(sql)
    cursor.execute(sql)
    db.commit()
    res = cursor.fetchall()
    reslen = len(res)
    return res, reslen

def getcinemaID(cinname):
    # 获取负责影院的ID
    msg = ''
    db, cursor = deal.connect2db()
    sql = "SELECT cinemaID from CinAdmin WHERE adminname = '{}'".format(cinname)
    cursor.execute(sql)
    db.commit()
    msg = 'done'
    cinemaID = cursor.fetchone()
    return msg, cinemaID