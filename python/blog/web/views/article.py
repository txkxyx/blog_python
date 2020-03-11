import datetime
from web import application, db
from web.service import article_service as a_s
from web.service.aws_service import S3
from web.forms.article.article_form import ArticleForm, ArticleView
from web.models.articles import Articles
from web.models.genres import Genres
from web.models.artile_genre import ArticleGenre
from flask import render_template, request, redirect
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

@application.route('/articles')
def list():
    articles = a_s.get_articles(a_s.all())
    return render_template('article/articles.html', articles=articles)

@application.route('/articles/<genre_id>')
def list_by_genre_id(genre_id):
    articles = a_s.get_articles(a_s.find_genreid(genre_id))
    genre = Genres.query.filter_by(id=genre_id).first()
    return render_template('article/articles.html',articles=articles, genre=genre)

@application.route('/article/post',methods=['GET','POST'])
@login_required
def post():
    form = ArticleForm()
    if request.method == 'GET':
        return render_template('article/post.html',form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            genres = form.genre.data.split(',')
            register_genres = a_s.class_genre(genres)
            img_url = S3().put_obj(form.image.data)
            article = Articles(form.title.data,form.body.data,form.summary.data,img_url,datetime.datetime.now(),current_user.id)
            try:
                a_s.post_article(article,register_genres,genres)
            except Exception:
                return render_template('article/post.html',form=form)
            return redirect('/articles')
        else:
            return render_template('article/post.html',form=form)

@application.route('/article/<id>',methods=['POST','GET'])
def article(id):
    article = a_s.find_id(id)
    genres = a_s.find_genres_aid(id)
    relations = a_s.find_relations(genres,id)
    return render_template('article/article.html',article=article,genres=genres, relations=relations)

@application.route('/article/edit',methods=['GET','POST'])
@login_required
def edit():
    form = ArticleForm()
    if request.method == 'GET':
        article = a_s.find_id(request.args.get('id'))
        genres = a_s.find_genres_aid(request.args.get('id'))
        return render_template('article/edit.html',form=form,article=article,genres=','.join([genre.name for genre in genres]))
    elif request.method == 'POST':
        genres = form.genre.data.split(',')
        register_genres = a_s.class_genre(genres)        
        article = a_s.find_id(form.id.data)
        if form.image.data is not None:
            S3().del_obj(article.img_url)
            article.img_url = S3().put_obj(form.image.data)
        article.title = form.title.data
        article.body = form.body.data
        article.summary = form.summary.data
        article.update_date = datetime.datetime.now()
        article.update_id = current_user.id
        article.version += 1
        try:
            a_s.post_article(article,register_genres,genres)
        except Exception:
            return render_template('article/edit.html',form=form,article=article)
        return redirect('/articles')
    
@application.route('/article/delete',methods=['POST'])
@login_required
def article_delete():
    form = ArticleForm()
    article = Articles.query.filter_by(id=form.id.data).first()
    article.delete_flg = True
    article.update_date = datetime.datetime.now()
    article.update_id = current_user.id
    article.version += 1
    try:
        db.session.add(article)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return render_template('article/edit.html',form=form,article=article)
    return redirect('/articles')
        