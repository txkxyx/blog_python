from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import flask_login
from flask_wtf.csrf import CSRFProtect
from config import Config

# Create Application
application = Flask(__name__)

# Set Config File
application.config.from_object(Config)
# Set CORS
CORS(application)
# Create Login Manger
login_manager = flask_login.LoginManager()
login_manager.init_app(application)

# Set CSRF Token
csrf = CSRFProtect(application)
# Set DB Migrate
db = SQLAlchemy(application)
migrate = Migrate(application, db)

import app
from web.views import auth, index, article
from web.models import users,genres,articles,artile_genre

from web.models.users import Users

@login_manager.user_loader
def load_user(user_id):
    return Users.query.filter_by(id=user_id).first()
