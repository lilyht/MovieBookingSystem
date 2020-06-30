#-*- coding=utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import dealwithdb as deal
import statistics
import captcha
import movie as mv
import cinema as cin
import courier
import morder
import admin
import courier as co
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
        toppopular = statistics.popularmovie()
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
        # print(adminRole)
        print(username)
        # 连接数据库，默认数据库用户名root，密码空
        if adminRole == None:
            return render_template('login.html', messages="roleempty")
        elif adminRole == 'SYSADMIN':  # 系统管理员
            sysadmin = admin.SysAdmin(username, password)
            msg = admin.SysAdmin.SysAdminLogin(sysadmin)
            return render_template('login.html', messages=msg, username=username, userRole=adminRole)

        elif adminRole == 'CINADMIN':  # 电影院管理员
            cinadmin = admin.CinAdmin(username, password)
            msg = admin.CinAdmin.CinAdminLogin(cinadmin)
            return render_template('login.html', messages=msg, username=username, userRole=adminRole)
        elif adminRole == 'COURIER':  # 送票员
            cour = co.Courier(username, password)
            msg = co.Courier.CourierLogin(cour)
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
        print('CinemaDetail-GET')
        return render_template('CinemaDetail.html')
    elif request.method == 'POST':
        # 从影院点击进来的是POST方法
        print('CinemaDetail-POST')
        cinemaID = request.form.get('cinemaID')
        c = cin.Cinema(cinemaID)
        cinema = c.getinfo()
        res, reslen = mv.selectbycinema(cinemaID)
        print(res)

        if reslen != 0:
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
        moviename = request.args.get('Movie')
        print(cinemaID)
        m = mv.Movie(moviename, cinemaID)
        msg, movieinfo = m.selectmovie()
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

        m = mv.Movie(movie, cinemaID)
        msg, movieinfo = m.selectmovie()

        if chara != imgchar:
            msg = 'captcha not correct'
            print(msg)
            return render_template('MovieDetail.html', movieinfo=movieinfo, messages=msg)
        print('验证码正确!')

        afare = request.form.get('afare')
        bfare = request.form.get('bfare')       
        buynum = request.form.get('buynum')
        name = request.form.get('name')
        addr = request.form.get('addr')
        phone = request.form.get('phone')
        seatrank = request.form.get('seatrank')
        tansactiontime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        afare = float(afare)
        bfare = float(bfare)
        buynum = int(buynum)
        print(buynum)
        # print(tansactiontime)
        print("{}-{}-{}-{}".format(name, addr, phone, seatrank))
        

        ordernum = morder.count()  # 总订单数
        orderID = str(ordernum[0]+1)
        maxseat =  100
        # print(ordernum[0])
        seatnum = ''
        for i in range (buynum):
            r = random.randint(0,maxseat)
            seatnum = seatrank + str(r) + ' ' + seatnum
        if seatrank == 'A':
            cost = buynum * afare
        else:
            cost = buynum * bfare

        myorder = morder.Morder(orderID, movie, cinemaID, seatrank, seatnum, phone, addr, 0, cost, tansactiontime)
        msg = myorder.insertmorder()        
        return render_template('MovieDetail.html', movieinfo=movieinfo, messages=msg)
    
@app.route('/MovieDetail2', methods=['GET', 'POST'])
def MovieDetail2():
    global chara
    msg = ''
    if request.method == 'GET':
        print('MovieDetail2 - GET')
        moviename = request.args.get('movie')
        m = mv.Movie(moviename, 0)
        msg, movieinfo = m.selectbymovie()
        print(movieinfo)
        # 查找含有该影片的影院
        msg, cinemaIDlist = m.selectcinema()
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
        m = mv.Movie(movie, 0)
        msg, movieinfo = m.selectbymovie()
        if chara != imgchar:   
            msg = 'captcha not correct'
            print(msg)
            return render_template('MovieDetail2.html', movieinfo=movieinfo, messages=msg)
        
        print('验证码正确!')
        
        print(cinemaID)
        print(type(cinemaID))
        
        afare = request.form.get('afare')
        bfare = request.form.get('bfare')
        buynum = request.form.get('buynum')
        name = request.form.get('name')
        addr = request.form.get('addr')
        phone = request.form.get('phone')
        seatrank = request.form.get('seatrank')
        tansactiontime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        afare = float(afare)
        bfare = float(bfare)
        buynum = int(buynum)

        ordernum = morder.count()  # 总订单数
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
        myorder = morder.Morder(orderID, movie, cinemaID, seatrank, seatnum, phone, addr, 0, cost, tansactiontime)
        msg = myorder.insertmorder()
        return render_template('MovieDetail2.html', movieinfo=movieinfo, messages=msg)

# 送票员页面
@app.route('/courierPage', methods=['GET', 'POST'])
def courierPage():
    msg = ''
    if request.method == 'GET':
        print('courierPage - GET')
        couriername =  request.args.get('couriername')
        msg, orderlist = co.getorderlist(couriername)
        # print(msg)
        return render_template('courierPage.html', messages=msg, orderlist=orderlist)
    else:
        if request.form["action"] == '送达确认':
            morderID = request.form.get('orderID')
            morder.finished(morderID)
            return render_template('courierPage.html', messages='OK')
        elif request.form["action"] == '取消订单':
            morderID = request.form.get('orderID')
            morder.delete(morderID)
            return render_template('courierPage.html', messages='DELETE')
    
    

# 系统管理员页面
@app.route('/sysadminPage', methods=['GET', 'POST'])
def sysadminPage():
    if request.method == 'GET':
        print('sysadminPage - GET')
        # movie = request.args.get('movie')
        return render_template('sysadminPage.html')
    

# 影院管理员页面
@app.route('/cinadminPage', methods=['GET', 'POST'])
def cinadminPage():
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
        f = request.files['the_file']

        if f and allowed_file(f.filename):
            filename = secure_filename(''.join(lazy_pinyin(f.filename)))
            f.save('static/images/' + filename)
            # flash("load file successfully!")
            imagesrc = ""
            imagesrc = 'static/images/' + filename
            print(imagesrc)
            cnum = cin.getcinemanum()  # 总影院数
            cinemaID = cnum[0] + 1
            c = cin.Cinema(cinemaID, cname, caddr, cphone, imagesrc, acapacity, bcapacity)
            c.insertcinema()
            
            return render_template("createCinema.html", messages="done")
        else:
            return render_template("createCinema.html", messages="unsuit")

# 系统管理员——指派电影院管理员
@app.route('/assign', methods=['GET', 'POST'])
def assign():
    if request.method == 'GET':
        print('assign - GET')
        res1, res1len = cin.waitforassign()
        res2, res2len = admin.getavailablecin()
        return render_template('assign.html', res1=res1, res2=res2, res1len=res1len, res2len=res2len)
    elif request.method == 'POST':
        cinemaID = request.form.get('cinemaname')
        adminname = request.form.get('adminname')

        c = admin.CinAdmin(adminname)
        msg = c.assigncinadmin(cinemaID)
        return render_template('assign.html', messages=msg)


# 影院管理员——更新影院信息
@app.route('/updatecininfo', methods=['GET', 'POST'])
def updatecininfo():
    if request.method == 'GET':
        print('updatecininfo - GET')
        cinname = request.args.get('cinname')        
        msg, cinemaID = admin.getcinemaID(cinname)  # 负责影院的ID
        c = cin.Cinema(cinemaID[0])
        cininfo = c.getinfo()
        return render_template('updatecininfo.html', res=cininfo)
    elif request.method == 'POST':
        print('updatecininfo - POST')
        # cinadminname = request.form.get('cinadminname')
        cname = request.form.get('cname')
        caddr = request.form.get('caddr')
        cphone = request.form.get('cphone')
        acapacity = request.form.get('acapacity')
        bcapacity = request.form.get('bcapacity')

        # 更新
        cin.updatecinema(cname, caddr, cphone, acapacity, bcapacity)
        
        db, cursor = deal.connect2db()
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
        msg, cinemaID = admin.getcinemaID(cinname)
        return render_template('uploadmovie.html', cinemaID=cinemaID[0])

    elif request.method == 'POST':
        movie = request.form.get('movie')
        if movie == '':
            print("kong")
            return render_template('uploadmovie.html', messages="empty")
        else:
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
            m = mv.Movie(movie, cinemaID, showtime, duration, screenshot, intro, trailer, afare, bfare)
            msg = m.insertmovie()
            return render_template('uploadmovie.html', messages=msg)


# 影院管理员——派送票员送票
@app.route('/delivery', methods=['GET', 'POST'])
def delivery():
    if request.method == 'GET':
        print('delivery - GET')
        cinname = request.args.get('cinname')
        print(cinname)
        msg, cinemaID = admin.getcinemaID(cinname)
        msg, res = morder.getorder(cinemaID[0])
        deliverylist = courier.getnamelist()
        return render_template('delivery.html', cinemaID=cinemaID[0], orderlist=res, deliverylist=deliverylist, messages=msg)
    elif request.method == 'POST':
        print('delivery - POST')
        orderID = request.form.get('orderID')
        couriername = request.form.get('couriername')
        print("订单{}--送票员：{}".format(orderID, couriername))

        db, cursor = deal.connect2db()
        sql1 = "UPDATE MOrder SET courier = '{}' WHERE orderID = '{}'".format(couriername, orderID)
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
        toppopular = statistics.popularmovie()  # 调用模块
        topcinema = statistics.popularcinema() #调用模块
        cinemanum = statistics.cinemaNum()
        movienum = statistics.movieNum()
        ordernum = statistics.orderNum()

        return render_template('analysis.html',cinemanum=cinemanum, movienum=movienum, ordernum=ordernum, toppopular=toppopular, topcinema=topcinema)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='9292')