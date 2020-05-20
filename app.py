#-*- coding=utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import sys
# 重新载入模块，得到更新后的模块
import importlib
importlib.reload(sys)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index')
def indexpage():
	return render_template('indexPage.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port='9292')