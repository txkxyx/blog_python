from web import application, db
from flask import render_template, redirect, request
from flask_login import login_user, login_required, logout_user, LoginManager
from werkzeug.security import check_password_hash, generate_password_hash
from web.forms.auth.login_form import LoginForm
from web.forms.auth.user_form import UserForm
from web.models.users import Users
from web.service import article_service as a_s

@application.route('/auth')
def auth():
    form = LoginForm()
    return render_template('auth/login.html', form=form)

@application.route('/auth/signup',methods=['POST','GET'])
def siginup():
    form = UserForm()
    if request.method == 'GET':
        return render_template('auth/signup.html',form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            if Users.query.filter_by(mail=form.mail.data).first():
                return render_template('auth/signup.html',form=form) 
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            user = Users(form.name.data,form.mail.data,hashed_password)
            try:
                db.session.add(user)
                db.session.commit()
            except Exception:
                db.session.rollback()
                return render_template('auth/signup.html',form=form) 
            finally:
                db.session.close()
            return redirect('/')
        else:
            return render_template('auth/signup.html',form=form)

@application.route('/auth/login',methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(mail = form.mail.data).first()
        if user:
            if not check_password_hash(user.password,form.password.data):
                return render_template('auth/login.html', form=form)
        else:
            return render_template('auth/login.html', form=form)
    else:
        return render_template('auth/login.html', form=form)
    login_user(user)
    return redirect('/auth/main')

@application.route('/auth/logout')
@login_required
def logout():
    logout_user()
    return redirect('/auth')

@application.route('/auth/main')
@login_required
def main():
    users = Users.query.all()
    articles = a_s.all()
    return render_template('auth/main.html',users=users,articles=articles)

@application.route('/auth/user/edit',methods=['POST','GET'])
@login_required
def user_edit():
    form = UserForm()
    if request.method == 'GET':
        user = Users.query.filter_by(id=request.args.get('id')).first()        
        return render_template('auth/useredit.html',user=user, form=form)
    if request.method == 'POST':
        user = Users.query.filter_by(id=form.id.data).first()
        user.mail = form.mail.data
        user.name = form.name.data
        user.version += 1
        try:
            db.session.add(user)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return render_template('auth/useredit.html',user=user, form=form)
        finally:
            db.session.close()
        return redirect('/auth/main')
    
@application.route('/auth/user/change',methods=['POST','GET'])
@login_required
def user_change():
    form = UserForm()
    if request.method == 'GET':
        if request.method == 'GET':
            user = Users.query.filter_by(id=request.args.get('id')).first()        
            return render_template('auth/userchange.html',user=user, form=form)
    if request.method == 'POST':
        user = Users.query.filter_by(id=form.id.data).first()
        if check_password_hash(user.password,generate_password_hash(form.now_password.data,method='sha256')):
            return render_template('auth/userchange.html',user=user, form=form)
        user.password = generate_password_hash(form.password.data,method='sha256')
        try:
            db.session.add(user)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return render_template('auth/userchange.html',user=user, form=form)
        finally:
            db.session.close()
        return redirect('/auth/main')

@application.route('/auth/user/delete',methods=['POST'])
@login_required
def user_delete():
    form = UserForm()
    user = Users.query.filter_by(id=form.id.data).first()
    try:
        db.session.delete(user)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return render_template('auth/userchange.html',user=user, form=form)
    finally:
        db.session.close()
    return redirect('/auth/main')