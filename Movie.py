# coding:utf-8  
import os  
import sys
import dealwithdb as deal
import importlib
importlib.reload(sys)
import MySQLdb
import importlib

class Movie():
    def __init__(self, movie, cinemaID, showtime='', duration=0, screenshot='', intro='', trailer='', afare=0, bfare=0):
        self.movie = movie
        self.cinemaID = int(cinemaID)
        self.showtime = showtime
        self.duration = duration
        self.screenshot = screenshot
        self.intro = intro
        self.trailer = trailer
        self.afare = afare
        self.bfare = bfare
        print('初始化')

    def insertmovie(self):
        msg = ''
        db, cursor = deal.connect2db()
        sql = "INSERT into Movie values ('{}', {}, '{}', {}, '{}', '{}', '{}', {}, {} );".format(self.movie, self.cinemaID, self.showtime, self.duration, self.screenshot, self.intro, self.trailer, self.afare, self.bfare)
        print(sql)
        cursor.execute(sql)
        db.commit()
        print('Insert into Movie seccessfully!')
        msg = 'done'
        return msg
    
    def selectmovie(self):
        msg = ''
        db, cursor = deal.connect2db()
        sql = "SELECT * from Movie WHERE cinemaID = {} AND movie = '{}'".format(self.cinemaID, self.movie)
        cursor.execute(sql)
        db.commit()
        movieinfo = cursor.fetchone()
        msg = 'done'
        return msg, movieinfo
    
    def selectbymovie(self):
        msg = ''
        db, cursor = deal.connect2db()
        sql = "SELECT * from Movie WHERE movie = '{}'".format(self.movie)
        cursor.execute(sql)
        db.commit()
        movieinfo = cursor.fetchone()
        msg = 'done'
        return msg, movieinfo


    def selectcinema(self):
        # 查找含有该影片的影院
        msg = ''
        db, cursor = deal.connect2db()
        sql = "SELECT DISTINCT M.cinemaID, C.cname FROM MOVIE M, CINEMA C WHERE M.movie = '{}' AND M.cinemaID = C.cinemaID;".format(self.movie)
        print(sql)
        cursor.execute(sql)
        db.commit()
        cinemaIDlist = cursor.fetchall()
        return msg, cinemaIDlist

def selectbycinema(cinemaID):
    msg = ''
    db, cursor = deal.connect2db()
    sql = "SELECT * from Movie WHERE cinemaID = {}".format(cinemaID)
    cursor.execute(sql)
    db.commit()
    res = cursor.fetchall()
    reslen = len(res)
    return res, reslen

if __name__ == "__main__":
    pass