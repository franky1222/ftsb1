# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/1 14:50
# @File    : Start.py
"""
应用启动类
"""

from flask import Flask, render_template, flash, url_for, redirect, Blueprint
from flask_bootstrap import Bootstrap

from flask_moment import Moment
from flask_login import LoginManager, login_user, UserMixin, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
import sys
import importlib
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

# 解决flash的一个bug
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    importlib.reload(sys)
    sys.setdefaultencoding(defaultencoding)

app = Flask(__name__)

# 各项插件的配置
app.config['SECRET_KEY'] = 'kkk'	# Flask-wtf表单，flash需要
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:jionsuiji123.@localhost/testdb'  # 配置数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['SQLALCHEMY_POOL_SIZE'] = 100
db = SQLAlchemy()
db.init_app(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
login_manger = LoginManager()
login_manger.session_protection = 'strong'
login_manger.login_view = 'blog.login'
login_manger.init_app(app)


@login_manger.user_loader
def load_user(user_id):
    from usermodel import Users
    return Users.query.get(int(user_id))


"""
蓝图注册
"""


def init():
    from python import blog
    import pymysql
    pymysql.install_as_MySQLdb()
    app.register_blueprint(blueprint=blog, url_prefix='/blog')


if __name__ == '__main__':
    init()
    app.run(port=8080,debug=True)