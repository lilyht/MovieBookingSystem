# coding:utf-8  
import os  
import sys
import importlib
importlib.reload(sys)
import MySQLdb
import importlib
import dealwithdb as deal

class SysAdmin():
    def __init__(self, adminname, password):
        self.adminname = adminname
        self.password = password
    

class CinAdmin():
    def __init__(self, adminname, password, cinemaID):
        self.adminname = adminname
        self.password = password
        self.cinemaID = cinemaID

class courier():
    def __init__(self, name, password, cinemaID):
        self.name = name
        self.password = password
        
def SysAdminLogin(username, password):
    db, cursor = deal.connect2db()
    sql = "SELECT * from SYSADMIN where adminname = '{}' and password = '{}'".format(username, password)
    cursor.execute(sql)
    db.commit()
    res = cursor.fetchall()
    num = 0
    for row in res:
        num = num + 1
    # 如果存在该管理员且密码正确
    if num == 1:
        print("登录成功！欢迎系统管理员！")
        msg = "done1"
    else:
        print("您没有系统管理员权限或登录信息出错。")
        msg = "fail1"
    return msg

def CinAdminLogin(username, password):
    db, cursor = deal.connect2db()
    sql = "SELECT * from CINADMIN where adminname = '{}' and password='{}'".format(username, password)
    cursor.execute(sql)
    db.commit()
    res = cursor.fetchall()
    num = 0
    for row in res:
        num = num + 1
    # 如果存在该电影院管理员且密码正确
    if num == 1:
        print("登录成功！欢迎电影院管理员！")
        msg = "done2"
    else:
        print("您没有电影院管理员权限或登录信息出错。")
        msg = "fail2"

    return msg


if __name__ == "__main__":
    pass