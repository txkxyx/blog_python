# coding: utf-8
from web import db

class Genres(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    version = db.Column(db.Integer, nullable=True)
    __mapper_args__ = {'version_id_col': version} 
    
    
    def __init__(self,name,version=0):
        self.name = name
        self.version = version