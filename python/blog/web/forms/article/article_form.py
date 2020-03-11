# coding: utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired, Length
from wtforms.widgets import TextArea

class ArticleForm(FlaskForm):
    '''
    記事登録・編集用フォーム
    '''
    id = IntegerField('Id')
    title = StringField('タイトル',validators=[DataRequired(),Length(min=1,max=255)])
    body = StringField('本文',validators=[DataRequired()],widget=TextArea())
    summary = StringField('説明', validators=[DataRequired(), Length(min=50,max=150)])
    image = FileField('ヘッダー画像')
    genre = StringField('ジャンル') 
    delete_flg = BooleanField('Delete Flag')
    submit = "Post"
    delete = "Delete"

class ArticleView():
    '''
    記事表示用フォーム
    '''
    
    def __init__(self, id, title, body, summary, img_url, delete_flg, insert_date, genres):
        self.id = id
        self.title = title
        self.body = body
        self.summary = summary
        self.img_url = img_url
        self.delete_flg = delete_flg
        self.insert_date = insert_date
        self.genres = genres
        
    
    