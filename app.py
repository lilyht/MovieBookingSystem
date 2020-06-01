#-*- coding=utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import datetime
import time
import string
import random;
import os
import sys
# 重新载入模块，得到更新后的模块
import MySQLdb
import importlib
importlib.reload(sys)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def indexpage():
    if request.method == 'GET':
        return render_template('indexPage.html')
  

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('adminname')
        password = request.form.get('password')
        adminRole = request.form.get('adminRole')
        print(adminRole)
        print(username)
        # 连接数据库，默认数据库用户名root，密码空
        db = MySQLdb.connect("localhost", "root", "", "MBDB", charset='utf8')

        if adminRole == 'SYSADMIN':  # 系统管理员
            cursor = db.cursor()
            try:
                cursor.execute("use MBDB")
            except:
                print("Error: unable to use database!")
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
            print(msg)
            return render_template('login.html', messages=msg, username=username, userRole=adminRole)

        elif adminRole == 'CINADMIN':  # 电影院管理员
            cursor = db.cursor()
            try:
                cursor.execute("use CINADMIN")
            except:
                print("Error: unable to use database!")
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
            return render_template('login.html', messages=msg, username=username, userRole=adminRole)

# 影片列表
@app.route('/MovieList', methods=['GET', 'POST'])
def MovieList():
    msg = ''
    # 连接数据库，默认数据库用户名root，密码空
    db = MySQLdb.connect("localhost", "root", "", "MBDB", charset='utf8')
    cursor = db.cursor()
    try:
        cursor.execute("use MBDB")
    except:
        print("Error: unable to use database!")
    sql = "SELECT * from Movie"
    cursor.execute(sql)
    db.commit()
    res = cursor.fetchall()

    if request.method == 'GET':
        print('GET')
        if len(res) != 0:
            msg = "done"
            print(msg)
            return render_template('MovieList.html', result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('MovieList.html', messages=msg)
    # elif request.method == 'POST':
    #     print('POST')
    #     # TODO: msg为空，待解决
    #     cinemaID = request.form.get('cinemaID')
    #     # print(cinemaID)
    #     print(msg)
    #     return render_template('CameraDetail.html' ,messages=msg, cinemaID=cinemaID)

# 影院列表
@app.route('/CinemaList', methods=['GET', 'POST'])
def CinemaList():
    msg = ''
    # 连接数据库，默认数据库用户名root，密码空
    db = MySQLdb.connect("localhost", "root", "", "MBDB", charset='utf8')
    cursor = db.cursor()
    try:
        cursor.execute("use MBDB")
    except:
        print("Error: unable to use database!")
    sql = "SELECT * from Cinema"
    cursor.execute(sql)
    db.commit()
    res = cursor.fetchall()

    if request.method == 'GET':
        print('GET')
        if len(res) != 0:
            msg = "done"
            print(msg)
            return render_template('CinemaList.html', result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('CinemaList.html', messages=msg)
    elif request.method == 'POST':
        print('POST')
        # TODO: msg为空，待解决
        cinemaID = request.form.get('cinemaID')
        # print(cinemaID)
        print(msg)
        return render_template('CinemaDetail.html' ,messages=msg, cinemaID=cinemaID)

# 影院详情
@app.route('/CinemaDetail', methods=['GET', 'POST'])
def CinemaDetail():
    if request.method == 'GET':
        print('GET')
        return render_template('CinemaDetail.html')
    elif request.method == 'POST':
        # 从影院点击进来的是POST方法
        print('POST')
        cinemaID = request.form.get('cinemaID')
        print(cinemaID)

        db = MySQLdb.connect("localhost", "root", "", "MBDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use MBDB")
        except:
            print("Error: unable to use database!")
        sql1 = "SELECT * from Cinema WHERE cinemaID = {}".format(cinemaID)
        cursor.execute(sql1)
        db.commit()
        cinema = cursor.fetchone()
        print(cinema)

        sql = "SELECT * from Movie WHERE cinemaID = {}".format(cinemaID)
        cursor.execute(sql)
        db.commit()
        res = cursor.fetchall()
        # print(res)
        if len(res) != 0:
            msg = "done"
            print(msg)
            return render_template('CinemaDetail.html', cinmea=cinema, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('CinemaDetail.html', cinmea=cinema, messages=msg)

@app.route('/MovieDetail', methods=['GET', 'POST'])
def MovieDetail():
    msg = ''
    if request.method == 'GET':
        print('MovieDetail - GET')
        cinemaID = request.args.get('CinemaID')
        movie = request.args.get('Movie')
        print(cinemaID)
        print(movie)
        db = MySQLdb.connect("localhost", "root", "", "MBDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use MBDB")
        except:
            print("Error: unable to use database!")
        sql = "SELECT * from Movie WHERE cinemaID = {} AND movie = '{}'".format(cinemaID, movie)
        cursor.execute(sql)
        db.commit()
        movieinfo = cursor.fetchone()
        print(movieinfo)
        msg = 'done'
        return render_template('MovieDetail.html', movieinfo=movieinfo, messages=msg)   
    elif request.method == 'POST':
        print("用户提交订单")
        movie = request.form.get('Movie')
        cinemaID = request.form.get('CinemaID')
        price = request.form.get('price')
        price = float(price)
        buynum = request.form.get('buynum')
        buynum = int(buynum)
        print(buynum)
        name = request.form.get('name')
        addr = request.form.get('addr')
        phone = request.form.get('phone')
        seatrank = request.form.get('seatrank')
        tansactiontime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # print(tansactiontime)
        print("{}-{}-{}-{}".format(name, addr, phone, seatrank))

        db = MySQLdb.connect("localhost", "root", "", "MBDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use MBDB")
        except:
            print("Error: unable to use database!")
        sql = "SELECT count(*) from MOrder"
        cursor.execute(sql)
        db.commit()
        ordernum = cursor.fetchone()  # 总订单数
        # print(ordernum[0])
        seatnum = ''
        for i in range (buynum):
            r = random.randint(0,100)
            seatnum = seatrank + str(r) + ' ' + seatnum
        print(seatnum)
        cost = buynum * price
        print(cost)
        orderID = str(ordernum[0]+1)
        sql = "INSERT into MOrder values ('{}', '{}', {}, '{}', '{}', '{}', '{}', {}, {}, '{} ');".format(orderID, movie, int(cinemaID), seatrank, seatnum, phone, addr, 0, cost, tansactiontime)
        print(sql)
        cursor.execute(sql)
        db.commit()
        # TODO: 提示提交订单成功，等待派送，考完试再写这块就行

        return render_template('index.html')
    
@app.route('/MovieDetail2', methods=['GET', 'POST'])
def MovieDetail2():
    msg = ''
    if request.method == 'GET':
        print('MovieDetail2 - GET')
        movie = request.args.get('movie')
        print(movie)
        db = MySQLdb.connect("localhost", "root", "", "MBDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use MBDB")
        except:
            print("Error: unable to use database!")
        sql = "SELECT * from Movie WHERE movie = '{}'".format(movie)
        print(sql)
        cursor.execute(sql)
        db.commit()
        movieinfo = cursor.fetchone()
        print(movieinfo)
        msg = 'done'

        # 查找含有该影片的影院
        sql = "SELECT DISTINCT M.cinemaID, C.cname FROM MOVIE M, CINEMA C WHERE M.movie = '{}' AND M.cinemaID = C.cinemaID;".format(movie)
        print(sql)
        cursor.execute(sql)
        db.commit()
        cinemaIDlist = cursor.fetchall()
        return render_template('MovieDetail2.html', movieinfo=movieinfo, messages=msg, cinemaIDlist=cinemaIDlist)   
    elif request.method == 'POST':
        print("用户提交订单2")
        movie = request.form.get('Movie')
        cinemaID = request.form.get('cinemaname')
        print(cinemaID)
        print(type(cinemaID))
        db = MySQLdb.connect("localhost", "root", "", "MBDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use MBDB")
        except:
            print("Error: unable to use database!")
        
        price = request.form.get('price')
        price = float(price)
        buynum = request.form.get('buynum')
        buynum = int(buynum)
        print(buynum)
        name = request.form.get('name')
        addr = request.form.get('addr')
        phone = request.form.get('phone')
        seatrank = request.form.get('seatrank')
        tansactiontime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # print(tansactiontime)
        print("{}-{}-{}-{}".format(name, addr, phone, seatrank))

        sql = "SELECT count(*) from MOrder"
        cursor.execute(sql)
        db.commit()
        ordernum = cursor.fetchone()  # 总订单数
        # print(ordernum[0])
        seatnum = ''
        for i in range (buynum):
            r = random.randint(0,100)
            seatnum = seatrank + str(r) + ' ' + seatnum
        print(seatnum)
        cost = buynum * price
        print(cost)
        orderID = str(ordernum[0]+1)
        sql = "INSERT into MOrder values ('{}', '{}', {}, '{}', '{}', '{}', '{}', {}, {}, '{} ');".format(orderID, movie, int(cinemaID), seatrank, seatnum, phone, addr, 0, cost, tansactiontime)
        print(sql)
        cursor.execute(sql)
        db.commit()
        # TODO: 提示提交订单成功，等待派送，考完试再写这块

        return render_template('index.html')


# def check():
#     if request.method == 'POST':
#         print('check - POST')
#         name = request.form.get(['name'])
#         print(name)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port='9292')