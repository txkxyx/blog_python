# coding: utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired,Length

class LoginForm(FlaskForm):
    '''
    ログインページ用フォーム
    '''
    mail = StringField('Email',validators=[DataRequired(),Length(min=6,max=255)])
    password = PasswordField('Password', validators=[Length(min=8,max=25),DataRequired()])
    submit = 'Login'
    