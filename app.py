#-*- coding=utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import datetime
import time
import string
import random
import os
import sys
# 重新载入模块，得到更新后的模块
import MySQLdb
import importlib
importlib.reload(sys)

UPLOAD_FOLDER = '/static/images'
ALLOWED_EXTENSIONS = set(['jpg', 'png'])


app = Flask(__name__)
# app.secret_key = 'some_secret'


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def indexpage():
    if request.method == 'GET':
        return render_template('indexPage.html')
  
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


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

# 系统管理员页面
@app.route('/sysadminPage', methods=['GET', 'POST'])
def sysadminPage():
    msg = ''
    if request.method == 'GET':
        print('sysadminPage - GET')
        # movie = request.args.get('movie')
        return render_template('sysadminPage.html') 

# 影院管理员页面
@app.route('/cinadminPage', methods=['GET', 'POST'])
def cinadminPage():
    msg = ''
    if request.method == 'GET':
        print('cinadminPage - GET')
        # movie = request.args.get('movie')
        return render_template('cinadminPage.html') 

# 系统管理员——创建新影院
@app.route('/createCinema', methods=['GET', 'POST'])
def createCinema():
    if request.method == 'GET':
        print('createCinema - GET')
        # movie = request.args.get('movie')
        return render_template('createCinema.html') 
    elif request.method == 'POST':
        print('createCinema - POST')
        cname = request.form.get('cname')
        caddr = request.form.get('caddr')
        cphone = request.form.get('cphone')
        acapacity = request.form.get('acapacity')
        bcapacity = request.form.get('bcapacity')
        # print("{}-{}-{}-{}-{}".format(cname, caddr, cphone, acapacity, bcapacity))
        f = request.files['the_file']

        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save('static/images/' + filename)
            # flash("load file successfully!")
            imagesrc = ""
            imagesrc = 'static/images/' + filename
            print(imagesrc)

            # 查库
            db = MySQLdb.connect("localhost", "root", "", "MBDB", charset='utf8')
            cursor = db.cursor()
            try:
                cursor.execute("use MBDB")
            except:
                print("Error: unable to use database!")
            sql1 = "SELECT MAX(cinemaID) from Cinema"
            cursor.execute(sql1)
            db.commit()
            cnum = cursor.fetchone()  # 总影院数
            cinemaID = cnum[0] + 1
            
            sql = "INSERT INTO Cinema VALUES ({}, '{}', '{}', '{}', '{}', {}, {})".format(cinemaID, cname, caddr, cphone, imagesrc, acapacity, bcapacity)
            cursor.execute(sql)
            db.commit()
            return render_template("createCinema.html", messages="done")
        else:
            return render_template("createCinema.html", messages="unsuit")

# 系统管理员——指派电影院管理员
@app.route('/assign', methods=['GET', 'POST'])
def assign():
    if request.method == 'GET':
        print('assign - GET')
        db = MySQLdb.connect("localhost", "root", "", "MBDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use MBDB")
        except:
            print("Error: unable to use database!")

        # 查询待分配电影院
        sql = "select C.cinemaID, C.cname from cinema C WHERE C.cinemaID not in (select distinct CA.cinemaID from CinAdmin CA WHERE CA.cinemaID is not NULL);"
        print(sql)
        cursor.execute(sql)
        db.commit()
        res1 = cursor.fetchall()
        res1len = len(res1)
        print(res1len)

        # 查询空闲电影院管理员
        sql2 = "SELECT * from CinAdmin WHERE cinemaID is NULL"
        print(sql2)
        cursor.execute(sql2)
        db.commit()
        res2 = cursor.fetchall()
        res2len = len(res2)
        print(res2len)
        return render_template('assign.html', res1=res1, res2=res2, res1len=res1len, res2len=res2len)
    elif request.method == 'POST':
        cinemaID = request.form.get('cinemaname')
        adminname = request.form.get('adminname')
        print(cinemaID)
        print(adminname)
        db = MySQLdb.connect("localhost", "root", "", "MBDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use MBDB")
        except:
            print("Error: unable to use database!")

        # 查询待分配电影院
        sql = "UPDATE CinAdmin SET cinemaID = {} WHERE adminname = '{}'".format(cinemaID, adminname)
        print(sql)
        cursor.execute(sql)
        db.commit()
        msg = 'done'
        return render_template('assign.html', messages=msg)


# 影院管理员——更新影院信息
@app.route('/updatecininfo', methods=['GET', 'POST'])
def updatecininfo():
    if request.method == 'GET':
        print('updatecininfo - GET')
        msg = ''
        db = MySQLdb.connect("localhost", "root", "", "MBDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use MBDB")
        except:
            print("Error: unable to use database!")
        #TODO: 获取参数、更新影院信息
        sql1 = "SELECT cinemaID from CinAdmin WHERE adminname = '{}'".format()
        cursor.execute(sql1)
        db.commit()
        cnum = cursor.fetchone()  # 总影院数
        
        return render_template('updatecininfo.html', messages=msg, result=res)
    elif request.method == 'POST':
        print('updatecininfo - POST')
        cname = request.form.get('cname')
        caddr = request.form.get('caddr')
        cphone = request.form.get('cphone')
        acapacity = request.form.get('acapacity')
        bcapacity = request.form.get('bcapacity')
        # print("{}-{}-{}-{}-{}".format(cname, caddr, cphone, acapacity, bcapacity))
        f = request.files['the_file']

        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save('static/images/' + filename)
            # flash("load file successfully!")
            imagesrc = ""
            imagesrc = 'static/images/' + filename
            print(imagesrc)

            db = MySQLdb.connect("localhost", "root", "", "MBDB", charset='utf8')
            cursor = db.cursor()
            try:
                cursor.execute("use MBDB")
            except:
                print("Error: unable to use database!")
            sql1 = "SELECT MAX(cinemaID) from Cinema"
            cursor.execute(sql1)
            db.commit()
            cnum = cursor.fetchone()  # 总影院数
            cinemaID = cnum[0] + 1
            
            sql = "INSERT INTO Cinema VALUES ({}, '{}', '{}', '{}', '{}', {}, {})".format(cinemaID, cname, caddr, cphone, imagesrc, acapacity, bcapacity)
            cursor.execute(sql)
            db.commit()
            return render_template("updatecininfo.html", messages="done")
        else:
            return render_template("updatecininfo.html", messages="unsuit")

# def check():
#     if request.method == 'POST':
#         print('check - POST')
#         name = request.form.get(['name'])
#         print(name)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port='9292')