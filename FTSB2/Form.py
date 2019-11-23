# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/1 14:46
# @File    : Form.py
"""
表单类
"""

from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired,Length,Regexp,EqualTo
from wtforms import ValidationError
from flask_wtf import FlaskForm
from usermodel import Users


# 登录表单
class Login_Form(FlaskForm):
    userID = StringField('账号', validators=[DataRequired(), Length(6, 12), Regexp('\d{6,8}', message='格式错误，账号由6-8位数字组成')])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 16),Regexp('\w{6,16}', message='格式错误，密码由6-16位数字、字母和下划线组成')])
    submit = SubmitField('登录')


# 注册表单
class Register_Form(FlaskForm):
    userID = StringField('用户账号',validators=[DataRequired(), Length(6, 12), Regexp('\d{6,8}', message='格式错误，账号由6-8位数字组成')])
    password = PasswordField('用户密码', validators=[DataRequired(), Length(6, 16),Regexp('\w{6,16}', message='格式错误，密码由6-16位数字、字母和下划线组成')])
    checkPassword = PasswordField('确认密码', validators=[DataRequired(), Length(6, 16),Regexp('\w{6,16}', message='格式错误，密码由6-16位数字、字母和下划线组成'),EqualTo('password')])
    #userName = StringField('用户昵称', validators=[DataRequired(), Length(1, 10),Regexp('[\u4e00-\u9fa5]{1,10}', message='格式错误，昵称由1-10位中文组成')])
    #phoneNumber = StringField('手机号码',validators=[DataRequired(), Length(11), Regexp('\d{11}', message='格式错误，电话由11位数字组成')])
    submit=SubmitField('注册')

    def validate_userID(self,field):
        if Users.query.filter_by(userID=field.data).first():
            raise ValidationError('The userID is already in use.')
    '''def validate_phoneNumber(self,field):
        if Users.query.filter_by(phoneNumber=field.data).first():
            raise ValidationError('The phoneNumber is already in use.')
'''
class change_password_Form(FlaskForm):
    password = PasswordField('原密码', validators=[DataRequired(), Length(6, 16),Regexp('\w{6,16}', message='格式错误，密码由6-16位数字、字母和下划线组成')])
    new_password = PasswordField('新密码', validators=[DataRequired(), Length(6, 16),Regexp('\w{6,16}', message='格式错误，密码由6-16位数字、字母和下划线组成')])
    checkPassword = PasswordField('确认新密码', validators=[DataRequired(), Length(6, 16),Regexp('\w{6,16}', message='格式错误，密码由6-16位数字、字母和下划线组成'),EqualTo('new_password')])
    submit = SubmitField('确认')