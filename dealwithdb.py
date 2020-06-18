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

class MOVIE():
    def __init__(self, movie, cinemaID, showtime, duration, screenshot, intro, trailer, fare):
        self.movie = movie
        self.cinemaID = cinemaID
        self.showtime = showtime
        self.duration = duration
        self.screenshot = screenshot
        self.intro = intro
        self.trailer = trailer
        self.fare = fare
        print('初始化')

    def insertmovie(self):
        msg = ''
        db, cursor = connect2db()
        sql = "INSERT into Movie values ('{}', {}, '{}', {}, '{}', '{}', '{}', {} );".format(self.movie, self.cinemaID, self.showtime, self.duration, self.screenshot, self.intro, self.trailer, self.fare)
        print(sql)
        cursor.execute(sql)
        db.commit()
        print('Insert into Movie seccessfully!')
        msg = 'done'
        return msg

class CINEMA():
    def __init__(self, cinemaID, cname, caddr, cphone, imagesrc, acapacity, bcapacity):
        self.cinemaID = cinemaID
        self.cname = cname
        self.caddr = caddr
        self.cphone = cphone
        self.imagesrc = imagesrc
        self.acapacity = acapacity
        self.bcapacity = bcapacity
        print('初始化')
        
    def insertcinema(self):
        db, cursor = connect2db()
        sql = "INSERT into Cinema values ({}, '{}', '{}', '{}', '{}', {}, {} );".format(self.cinemaID, self.cname, self.caddr, self.cphone, self.imagesrc, self.acapacity, self.bcapacity)
        print(sql)
        cursor.execute(sql)
        db.commit()
        print('Insert into Cinema seccessfully!')




if __name__ == "__main__":
    pass