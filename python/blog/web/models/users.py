# coding: utf-8
from web import db
from flask_login import UserMixin

class Users(db.Model,UserMixin):
    __tablename__ = 'users' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    mail = db.Column(db.String(255))
    password = db.Column(db.String(255))
    version = db.Column(db.Integer, nullable=True)
    __mapper_args__ = {'version_id_col': version}
    
    def __init__(self,name,mail,password,version=0):
        self.name = name
        self.mail = mail
        self.password = password
        self.version = version
