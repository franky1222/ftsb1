# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/1 14:45
# @File    : Model.py
"""
数据模型
"""

from flask_login import LoginManager, login_user, UserMixin, logout_user, login_required
from Start import login_manger
from Start import db


class Users(UserMixin, db.Model):
    __tablename__ = 'users'  # 对应mysql数据库表
    userID = db.Column(db.Integer, primary_key=True, index=True)
    password = db.Column(db.String(16), nullable=False)
    userName = db.Column(db.String(10), nullable=False)
    #phoneNumber = db.Column(db.Integer, unique=True, nullable=False)

    regDate = db.Column(db.DateTime)
    isVip = db.Column(db.Integer)
    vDate = db.Column(db.DateTime)
    valDate = db.Column(db.DateTime)
    money = db.Column(db.Numeric(6,2))
    money_wait = db.Column(db.Numeric(6,2))
    PDF = db.Column(db.Integer)
    photo = db.Column(db.Integer)

    def get_regDate(self):
        return self.regDate

    def get_isVip(self):
        return self.isVip

    def get_vDate(self):
        return self.vDate

    def get_valDate(self):
        return self.valDate

    def set_regDate(self, regDate):
        self.regDate = regDate

    def set_isVip(self, isVip):
        self.isVip = isVip

    def set_vDate(self, vDate):
        self.vDate = vDate

    def set_valDate(self, valDate):
        self.valDate = valDate

    def __init__(self, userID, password):
        self.userID = userID
        self.password = password
        self.isVip = 0
        self.money = 0
        self.money_wait = 0
        self.PDF = 0
        self.photo = 0

    def set_pdf(self, pdf):
        self.PDF = pdf

    def set_photo(self, photo):
        self.photo = photo

    def get_id(self):
        return self.userID

    def get_userName(self):
        return self.userName

    def get_password(self):
        return self.password

    def get_phoneNumber(self):
        return self.phoneNumber

    def set_userID(self, userID):
        self.userID = userID

    def set_userName(self, userName):
        self.userName = userName

    def set_passwrod(self, password):
        self.password = password

    def set_phoneNumber(self, phoneNumber):
        self.phoneNumber = phoneNumber
		
    def get_money(self):
        return self.money

    def get_money_wait(self):
        return self.money_wait

    def set_money(self, money):
        self.money = money

    def set_money_wait(self, money_wait):
        self.money_wait = money_wait

	

class Charges(UserMixin, db.Model):
    __tablename__ = 'charge'  # 对应mysql数据库表
    cid = db.Column(db.Integer, primary_key=True, index=True)
    cdate = db.Column(db.DateTime, nullable=False)
    uid = db.Column(db.Integer, index=True, nullable=False)
    cmoney = db.Column(db.Integer, index=True, nullable=False)

    def __init__(self, cid, cdate, uid, cmoney):
        self.cid = cid
        self.cdate = cdate
        self.uid = uid
        self.cmoney = cmoney

    def get_id(self):
        return self.cid

    def get_cdate(self):
        return self.cdate

    def get_uid(self):
        return self.uid

    def get_cmoney(self):
        return self.cmoney

    def set_cdate(self, cdate):
        self.cdate = cdate

    def set_uid(self, uid):
        self.uid = uid

    def set_cmoney(self, cmoney):
        self.cmoney = cmoney

    def __repr__(self):
        return '<charge %r>' % self.cid

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def __repr__(self):
        return '<User %r>' % self.userID

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def __del__(self):
        db.session.close()

##########################################################################overwrite
class Records(UserMixin, db.Model):
    __tablename__ = 'records'  # 对应mysql数据库表
    record = db.Column(db.Integer, primary_key=True, index=True)
    userID = db.Column(db.Integer, index=True, nullable=False)
    dateTime = db.Column(db.DateTime, nullable=False)
    type=db.Column(db.Integer, index=True, nullable=False)
    num=db.Column(db.Integer, index=True, nullable=True)
    name=db.Column(db.String(100), nullable=True)

    def __init__(self, record, userID, dateTime, type, num, name):
        self.record = record
        self.userID = userID
        self.dateTime = dateTime
        self.type = type
        self.num = num
        self.name = name
		
    def get_num(self):
        return self.num

    def get_name(self):
        return self.name

    def get_userID(self):
        return self.userID

    def get_record(self):
        return self.record

    def get_dateTime(self):
        return self.dateTime

    def get_type(self):
        return self.type

    def set_user(self,user):
        self.user = user

    def set_record(self,record):
        self.record = record

    def set_dateTime(self,dateTime):
        self.dateTime = dateTime

    def set_type(self,type):
        self.type = type

    def __repr__(self):
        return '<Records %r>' % self.record

    def __del__(self):
        db.session.close()
##############################################################################

class Words(UserMixin, db.Model):
    __tablename__ = 'words'  # 对应mysql数据库表
    no = db.Column(db.Integer, primary_key=True, index=True)
    word = db.Column(db.String(100))
    graph = db.Column(db.String(255))
    record = db.Column(db.Integer)

    def __init__(self, no, word, graph, record):
        self.no = no
        self.word = word
        self.graph = graph
        self.record = record

