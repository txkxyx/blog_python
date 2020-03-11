# coding: utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired,Length, EqualTo

class UserForm(FlaskForm):
    '''
    マスタ管理用フォーム
    '''
    id = IntegerField('Id')
    mail = StringField('Email',validators=[DataRequired(),Length(min=6,max=255)])
    name = StringField('Name', validators=[DataRequired(),Length(min=1,max=100)])
    password = PasswordField('Password', validators=[Length(min=8,max=25),DataRequired(),EqualTo('conf_password',message='Password must match')])
    conf_password = PasswordField('Confirm Password', validators=[Length(min=8,max=25),DataRequired()])
    now_password = StringField('Now Password')
    confirm = 'Confirm'
    submit = 'SignUp'
    edit = 'Edit'
    delete = 'Delete'