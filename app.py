#-*- coding=utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
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
    elif request.method == 'GET':
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



@app.route('/CameraList', methods=['GET', 'POST'])
def CameraList():
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
            return render_template('CameraList.html', result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('CameraList.html', messages=msg)
    elif request.method == 'POST':
        print('POST')
        # TODO: 跳转到相应的影院内部页面
        # TODO: msg为空，待解决
        cinemaID = request.form.get('cinemaID')
        # print(cinemaID)
        print(msg)
        return render_template('CameraDetail.html' ,messages=msg, cinemaID=cinemaID)

@app.route('/CameraDetail', methods=['GET', 'POST'])
def CameraDetail():
    if request.method == 'GET':
        print('GET')
        render_template('CameraDetail.html')
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
        cinmea = cursor.fetchone()
        print(cinmea)

        sql = "SELECT * from Movie WHERE cinemaID = {}".format(cinemaID)
        cursor.execute(sql)
        db.commit()
        res = cursor.fetchall()
        # print(res)
        if len(res) != 0:
            msg = "done"
            print(msg)
            return render_template('CameraDetail.html', cinmea=cinmea, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('CameraDetail.html', cinmea=cinmea, messages=msg)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port='9292')