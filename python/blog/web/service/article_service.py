import itertools
import copy
from sqlalchemy import desc
from web import db
from web.models.articles import Articles
from web.models.genres import Genres
from web.models.artile_genre import ArticleGenre
from web.forms.article.article_form import ArticleView

def all():
    '''
    全件検索
    '''
    articles = Articles.query.filter_by(delete_flg=False).order_by(desc(Articles.id)).all()
    return articles


def find_id(id):
    '''
    記事ID検索
    '''
    article = Articles.query.filter_by(id=id).first()
    return article

def get_articles(func):
    '''
    ArticleViewを取得
    '''
    return [ArticleView(a.id,a.title,a.body,a.summary,a.img_url,a.delete_flg,a.insert_date,find_genres_aid(a.id)) for a in func]


def find_genreid(genre_id):
    '''
    ジャンルID検索
    '''
    article_ids =[article_genre.article_id for article_genre in ArticleGenre.query.filter_by(genre_id=genre_id).all()]
    articles = Articles.query.filter(Articles.id.in_(article_ids)).filter_by(delete_flg=False).order_by(desc(Articles.id)).all()
    return articles
    
def find_genreid_notmine(genre_id,id):
    '''
    自記事以外のジャンルID検索
    '''
    article_ids =[article_genre.article_id for article_genre in ArticleGenre.query.filter_by(genre_id=genre_id).all()]
    articles = Articles.query.filter(Articles.id.in_(article_ids)).filter_by(delete_flg=False).filter(Articles.id!=id).order_by(desc(Articles.id)).all()
    return articles

def class_genre(input_genres):
    '''
    記事のジャンルで未登録のジャンルを抽出
    '''
    genres = Genres.query.all()
    # no duplicate list
    nd_list = input_genres.copy()
    for i_g, g in itertools.product(input_genres, genres):
        if i_g == g.name:
            nd_list.remove(i_g)
    return nd_list

def post_article(article,register_genres,genres):
    '''
    記事登録
    '''
    try:
        # 記事とジャンルの登録
        db.session.add(article)
        for g in register_genres:
            db.session.add(Genres(g))
        db.session.flush()
        
        # 記事とジャンルを紐づける
        genres = Genres.query.filter(Genres.name.in_(genres)).all() 
        article_genres = ArticleGenre.query.filter_by(article_id=article.id).all()
        # 登録されているジャンルと、削除するジャンルを分ける
        for g, a_g in itertools.product(genres, article_genres):
            if g.id == a_g.genre_id:
                genres.remove(g)
                article_genres.remove(a_g)
        # 新しいジャンルの紐づけ
        for g in genres:
            db.session.add(ArticleGenre(article.id,g.id))
        # ジャンルの紐づけの削除
        for a_g in article_genres:
            db.session.delete(a_g)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.close()
        
def find_genres_aid(id):
    '''
    記事のジャンルを取得する
    '''
    a_g = ArticleGenre.query.filter_by(article_id=id).order_by(desc(ArticleGenre.id)).all()
    genres = [Genres.query.filter_by(id=g.genre_id).first() for g in a_g]
    return genres


def find_relations(genres,id):
    '''
    関連記事を取得する
    '''
    relations = []
    for g in genres:
        for a in get_articles(find_genreid_notmine(g.id,id)):
            relations.append(a)
    result = []
    for a in relations:
        for r in result:
            if a.id == r.id:
                break
        result.append(a)
    return result