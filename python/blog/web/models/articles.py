# coding: utf-8
from web import db

class Articles(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text(), nullable=False)
    summary = db.Column(db.String(150),nullable=False)
    img_url = db.Column(db.String(255),nullable=False)
    insert_date = db.Column(db.DateTime, nullable=False)
    insert_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    update_date = db.Column(db.DateTime, nullable=True)
    update_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    delete_flg = db .Column(db.Boolean, nullable=False, default=False)
    version = db.Column(db.Integer, nullable=True)
    __mapper_args__ = {'version_id_col': version}
    
    def __init__(self,title,body,summary,img_url,insert_date,insert_id,version=0,update_date=None,update_id=None):
        self.title = title
        self.body = body
        self.summary = summary
        self.img_url = img_url
        self.insert_date = insert_date
        self.insert_id = insert_id
        self.version = version
        self.update_date = update_date
        self.update_id = update_id
    
    