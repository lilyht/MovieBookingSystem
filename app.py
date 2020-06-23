#-*- coding=utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import dealwithdb as deal
import role
import statistics
import captcha
import Movie
import MOrder
from pypinyin import lazy_pinyin
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
global chara

app = Flask(__name__)
app.jinja_env.auto_reload = True
# app.secret_key = 'some_secret'


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def indexpage():
    if request.method == 'GET':
        toppopular = statistics.popular()
        print(toppopular)
        return render_template('indexPage.html', toppopular=toppopular)
  
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
        if adminRole == 'SYSADMIN':  # 系统管理员
            msg = role.SysAdminLogin(username, password)
            return render_template('login.html', messages=msg, username=username, userRole=adminRole)

        elif adminRole == 'CINADMIN':  # 电影院管理员
            msg = role.CinAdminLogin(username, password)
            return render_template('login.html', messages=msg, username=username, userRole=adminRole)

# 影片列表
@app.route('/MovieList', methods=['GET', 'POST'])
def MovieList():
    msg = ''
    # 连接数据库，默认数据库用户名root，密码空
    db, cursor = deal.connect2db()
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

# 影院列表
@app.route('/CinemaList', methods=['GET', 'POST'])
def CinemaList():
    msg = ''
    db, cursor = deal.connect2db()
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

        db, cursor = deal.connect2db()
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

@app.route('/search_results', methods=['GET'])
def search_results():
    if request.method == 'GET':
        print('search')
        content = request.args.get('s')  # 获取搜索内容
        searchtype = request.args.get('searchtype')
        if searchtype == '1':
            print("search cinema")
            msg, resultlist = statistics.search(1, content)
            print(resultlist)
            return render_template('search-results.html', type=1, messages=msg, result=resultlist)
        else:
            print("search movie")
            msg, resultlist = statistics.search(2, content)
            return render_template('search-results.html', type=2, messages=msg, result=resultlist)


@app.route('/MovieDetail', methods=['GET', 'POST'])
def MovieDetail():
    global chara
    msg = ''
    if request.method == 'GET':
        print('MovieDetail - GET')
        cinemaID = request.args.get('CinemaID')
        movie = request.args.get('Movie')
        print(cinemaID)
        print(movie)
        m = Movie.MOVIE(movie, cinemaID)
        msg, movieinfo = m.selectmovie(cinemaID, movie)
        print(movieinfo)
        # 验证码
        chara = captcha.generate()
        print('get: {}'.format(chara))

        return render_template('MovieDetail.html', movieinfo=movieinfo, messages=msg)   

    elif request.method == 'POST':
        print("用户提交订单")
        movie = request.form.get('Movie')
        cinemaID = request.form.get('CinemaID')
        imgchar = request.form.get('captcha')
        print(chara)
        print(captcha)

        m = Movie.MOVIE(movie, cinemaID)
        msg, movieinfo = m.selectmovie(cinemaID, movie)

        if chara != imgchar:
            msg = 'captcha not correct'
            print(msg)
            return render_template('MovieDetail.html', movieinfo=movieinfo, messages=msg)
        
        print('验证码正确!')
        afare = request.form.get('afare')
        afare = float(afare)
        bfare = request.form.get('bfare')
        bfare = float(bfare)

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

        ordernum = MOrder.count()  # 总订单数
        orderID = str(ordernum[0]+1)
        # print(ordernum[0])
        seatnum = ''
        for i in range (buynum):
            r = random.randint(0,100)
            seatnum = seatrank + str(r) + ' ' + seatnum
        print(seatnum)

        if seatrank == 'A':
            cost = buynum * afare
        else:
            cost = buynum * bfare
        print(cost)
        myorder = MOrder.MORDER(orderID, movie, cinemaID, seatrank, seatnum, phone, addr, 0, cost, tansactiontime)
        msg = myorder.insertmorder()        
        return render_template('MovieDetail.html', movieinfo=movieinfo, messages=msg)
    
@app.route('/MovieDetail2', methods=['GET', 'POST'])
def MovieDetail2():
    global chara
    msg = ''
    if request.method == 'GET':
        print('MovieDetail2 - GET')
        movie = request.args.get('movie')
        print(movie)

        m = Movie.MOVIE(movie, 0)
        msg, movieinfo = m.selectbymovie(movie)
        print(movieinfo)
        # 查找含有该影片的影院
        msg, cinemaIDlist = m.selectcinema(movie)
        # 验证码
        chara = captcha.generate()
        print('get: {}'.format(chara))
        return render_template('MovieDetail2.html', movieinfo=movieinfo, messages=msg, cinemaIDlist=cinemaIDlist)   
    elif request.method == 'POST':
        print("用户提交订单2")
        imgchar = request.form.get('captcha')
        movie = request.form.get('Movie')
        cinemaID = request.form.get('cinemaname')
        print(chara)
        print(captcha)
        m = Movie.MOVIE(movie, 0)
        msg, movieinfo = m.selectbymovie(movie)
        if chara != imgchar:   
            msg = 'captcha not correct'
            print(msg)
            return render_template('MovieDetail2.html', movieinfo=movieinfo, messages=msg)
        
        print('验证码正确!')
        
        print(cinemaID)
        print(type(cinemaID))
        
        afare = request.form.get('afare')
        afare = float(afare)
        bfare = request.form.get('bfare')
        bfare = float(bfare)
        buynum = request.form.get('buynum')
        buynum = int(buynum)
        # print(buynum)
        name = request.form.get('name')
        addr = request.form.get('addr')
        phone = request.form.get('phone')
        seatrank = request.form.get('seatrank')
        tansactiontime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("{}-{}-{}-{}".format(name, addr, phone, seatrank))

        ordernum = MOrder.count()  # 总订单数
        orderID = str(ordernum[0]+1)
        # print(ordernum[0])
        seatnum = ''
        for i in range (buynum):
            r = random.randint(0,100)
            seatnum = seatrank + str(r) + ' ' + seatnum
        print(seatnum)

        if seatrank == 'A':
            cost = buynum * afare
        else:
            cost = buynum * bfare
        print(cost)
        myorder = MOrder.MORDER(orderID, movie, cinemaID, seatrank, seatnum, phone, addr, 0, cost, tansactiontime)
        msg = myorder.insertmorder()
        return render_template('MovieDetail2.html', movieinfo=movieinfo, messages=msg)

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
        # cname = request.args.get('cinname')
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
            db, cursor = deal.connect2db()

            sql1 = "SELECT MAX(cinemaID) from Cinema"
            cursor.execute(sql1)
            db.commit()
            cnum = cursor.fetchone()  # 总影院数
            cinemaID = cnum[0] + 1
            
            sql = "INSERT INTO Cinema VALUES ({}, '{}', '{}', '{}', '{}', {}, {})".format(\
                cinemaID, cname, caddr, cphone, imagesrc, acapacity, bcapacity)
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
        db, cursor = deal.connect2db()

        # 查询待分配电影院
        sql = ('select C.cinemaID, C.cname from cinema C WHERE C.cinemaID not in '
            '(select distinct CA.cinemaID from CinAdmin CA WHERE CA.cinemaID is not NULL);')
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

        db, cursor = deal.connect2db()

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

        db, cursor = deal.connect2db()

        #TODO: 获取参数、更新影院信息
        cinname = request.args.get('cinname')
        print(cinname)
        sql1 = "SELECT cinemaID from CinAdmin WHERE adminname = '{}'".format(cinname)
        cursor.execute(sql1)
        db.commit()
        cinemaID = cursor.fetchone()  # 负责影院的ID

        sql2 = "SELECT * from Cinema WHERE cinemaID = {}".format(cinemaID[0])
        cursor.execute(sql2)
        db.commit()
        cininfo = cursor.fetchone()
        return render_template('updatecininfo.html', messages=msg, res=cininfo)
    elif request.method == 'POST':
        print('updatecininfo - POST')
        # cinadminname = request.form.get('cinadminname')
        cname = request.form.get('cname')
        caddr = request.form.get('caddr')
        cphone = request.form.get('cphone')
        acapacity = request.form.get('acapacity')
        bcapacity = request.form.get('bcapacity')
        print("{}-{}-{}-{}-{}".format(cname, caddr, cphone, acapacity, bcapacity))
        
        db, cursor = deal.connect2db()
        sql = "UPDATE Cinema SET caddr='{}', cphone='{}', acapacity={}, bcapacity={} WHERE cname = '{}'".format(caddr, cphone, acapacity, bcapacity, cname)
        cursor.execute(sql)
        db.commit()

        sql1 = "SELECT CinAdmin.adminname FROM CinAdmin, Cinema WHERE cname='{}' AND CinAdmin.cinemaID = Cinema.cinemaID".format(cname)
        cursor.execute(sql1)
        db.commit()
        res = cursor.fetchone()
        cinadminname = res[0]
        print(cinadminname)

        return render_template("cinadminPage.html", messages="done", cinadminname=cinadminname)


# 影院管理员——上传影片信息
@app.route('/uploadmovie', methods=['GET', 'POST'])
def uploadmovie():
    if request.method == 'GET':
        print('uploadmovie - GET')
        cinname = request.args.get('cinname')
        print(cinname)
        db, cursor = deal.connect2db()
        sql1 = "SELECT cinemaID from CinAdmin WHERE adminname = '{}'".format(cinname)
        cursor.execute(sql1)
        db.commit()
        cinemaID = cursor.fetchone()  # 负责影院的ID
        print(cinemaID[0])

        return render_template('uploadmovie.html', cinemaID=cinemaID[0])

    elif request.method == 'POST':
        movie = request.form.get('movie')
        duration = request.form.get('duration')
        trailer = request.form.get('trailer')
        afare = request.form.get('afare')
        bfare = request.form.get('bfare')
        request.form.get('trailer')
        showday =  request.form.get('showday')
        showtime = request.form.get('showtime')
        showtime = showday + ' ' + showtime + ':00'
        intro = request.form.get('intro')
        f = request.files['the_file']
        if f and allowed_file(f.filename):
            filename = secure_filename(''.join(lazy_pinyin(f.filename)))
            f.save('static/images/' + filename)
            # flash("load file successfully!")
            screenshot = ""
            screenshot = 'static/images/' + filename
            print(screenshot)

        cinemaID = request.form.get('cinemaID')
        cinemaID = cinemaID[0]

        #创建影片对象
        m = Movie.MOVIE(movie, cinemaID, showtime, duration, screenshot, intro, trailer, afare, bfare)
        msg = m.insertmovie()
        return render_template('uploadmovie.html', messages=msg)


# 影院管理员——派送票员送票
@app.route('/delivery', methods=['GET', 'POST'])
def delivery():
    if request.method == 'GET':
        print('delivery - GET')
        cinname = request.args.get('cinname')
        print(cinname)
        db, cursor = deal.connect2db()
        sql1 = "SELECT cinemaID from CinAdmin WHERE adminname = '{}'".format(cinname)
        cursor.execute(sql1)
        db.commit()
        cinemaID = cursor.fetchone()  # 负责影院的ID
        print(cinemaID[0])

        sql2 = "SELECT * FROM MOrder WHERE isFinished = 0 AND cinemaID = {}".format(cinemaID[0])
        cursor.execute(sql2)
        db.commit()
        res = cursor.fetchall()
        reslen = len(res)
        if reslen == 0:
            msg = "empty"
        else:
            msg = "have"
        
        sql3 = "SELECT name FROM Courier"
        cursor.execute(sql3)
        db.commit()
        deliverylist = cursor.fetchall()  
        return render_template('delivery.html', cinemaID=cinemaID[0], orderlist=res, deliverylist=deliverylist, messages=msg)
    elif request.method == 'POST':
        print('delivery - POST')
        orderID = request.form.get('orderID')
        couriername = request.form.get('couriername')
        print("订单{}--送票员：{}".format(orderID, couriername))

        db, cursor = deal.connect2db()
        sql1 = "UPDATE MOrder SET isFinished = 1 WHERE orderID = '{}'".format(orderID)
        cursor.execute(sql1)
        db.commit()

        sql2 = "SELECT CinAdmin.adminname FROM CinAdmin, MOrder WHERE MOrder.orderID = '{}' AND CinAdmin.cinemaID = MOrder.cinemaID".format(orderID)
        cursor.execute(sql2)
        db.commit()
        res = cursor.fetchone()
        cinadminname = res[0]
        print(cinadminname)
        return render_template("cinadminPage.html", messages="done", cinadminname=cinadminname)


# 系统统计分析模块
@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    if request.method == 'GET':
        print('analysis - GET')
        toppopular = statistics.popular()  # 调用模块
        topcinema = statistics.popularcinema() #调用模块
        cinemanum = statistics.cinemaNum()
        movienum = statistics.movieNum()
        ordernum = statistics.orderNum()

        return render_template('analysis.html',cinemanum=cinemanum, movienum=movienum, ordernum=ordernum, toppopular=toppopular, topcinema=topcinema)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='9292')