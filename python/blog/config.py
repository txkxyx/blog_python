# coding: utf-8
import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@blog_db:3306/blog_db?charset=utf8'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@0.0.0.0:33306/blog_db?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(32)
    # limit upload file size : 1MB
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024