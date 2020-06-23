# coding:utf-8  
import os  
import sys
import importlib
importlib.reload(sys)
import MySQLdb
import importlib
import dealwithdb as deal

def cinemaNum():
    db, cursor = deal.connect2db()
    sql = "SELECT COUNT(*) FROM Cinema"
    cursor.execute(sql)
    db.commit()
    res = cursor.fetchone()
    return res[0]

def movieNum():
    db, cursor = deal.connect2db()
    sql = "SELECT COUNT(*) FROM Movie"
    cursor.execute(sql)
    db.commit()
    res = cursor.fetchone()
    return res[0]

def orderNum():
    db, cursor = deal.connect2db()
    sql = "SELECT COUNT(*) FROM MOrder"
    cursor.execute(sql)
    db.commit()
    res = cursor.fetchone()
    return res[0]

def popular():
    # 统计最受欢迎影片模块
    db, cursor = deal.connect2db()
    # sql1 = "SELECT O.movie, COUNT(orderID) as sales FROM MOrder O Group BY O.movie ORDER BY sales DESC;"
    # 返回前三条结果
    sql1 = ('SELECT O.movie as topsales, COUNT(distinct(orderID)) as sales, M.showtime, M.screenshot, M.intro, M.trailer, M.bfare '
            'FROM MOrder O, Movie M WHERE M.movie = O.movie Group BY O.movie ORDER BY sales DESC limit 3;')

    cursor.execute(sql1)
    db.commit()
    toppopular = cursor.fetchall()
    # 创建对象
    return toppopular

def popularcinema():
    # 统计最受欢迎电影院模块
    db, cursor = deal.connect2db()
    # 返回前三条结果
    sql1 = ('SELECT O.cinemaID, COUNT(distinct(orderID)) as sales, C.cname, C.imagesrc '
            'FROM MOrder O, Cinema C WHERE C.cinemaID = O.cinemaID Group BY O.cinemaID ORDER BY sales DESC limit 3;')

    cursor.execute(sql1)
    db.commit()
    topcinema = cursor.fetchall()
    return topcinema

def analysis():
    #TODO: 分析模块的函数
    return True

def search(type, content):
    msg = ''
    db, cursor = deal.connect2db()
    if type == 1:
        sql = "select * from Cinema where cname like '%{}%';".format(content)
        cursor.execute(sql)
        db.commit()
        cinemaresultlist = cursor.fetchall()
        if len(cinemaresultlist) != 0:
            msg = 'done'
        else:
            msg = 'none'
        return msg, cinemaresultlist
    elif type == 2:
        sql = "select * from Movie where movie like '%{}%';".format(content)
        cursor.execute(sql)
        db.commit()
        movieresultlist = cursor.fetchall()
        if len(movieresultlist) != 0:
            msg = 'done'
        else:
            msg = 'none'
        return msg, movieresultlist
    else:
        msg = 'error'
        return msg, ''

if __name__ == "__main__":
    pass