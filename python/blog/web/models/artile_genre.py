# coding: utf-8
from web import db

class ArticleGenre(db.Model):
    __tablename__ = 'article_genre'
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'), nullable=False)
    
    def __init__(self,article_id,genre_id):
        self.article_id = article_id
        self.genre_id = genre_id