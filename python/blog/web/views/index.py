from web import application, db
from web.forms.article.article_form import ArticleView
from web.service import article_service as a_s
from flask import request, jsonify, render_template

    

@application.route('/')
def index():
    articles = a_s.get_articles(a_s.all())
    return render_template('index.html',articles=articles)
