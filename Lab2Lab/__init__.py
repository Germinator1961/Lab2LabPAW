from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
#from flask_login import LoginManager
#from Lab2Lab.config import Config

db = SQLAlchemy()
DB_NAME = "l2l.db"

def create_app():
    app = Flask(__name__)

    #app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'   # TODO: Change in production
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #app.config.from_object(Config)
    #db.init_app(app)

    #from .views import views
    #from .auth import auth
    #app.register_blueprint(views, url_prefix='/')
    #app.register_blueprint(auth, url_prefix='/')

    #from .models import User
    #create_database(app)

    #login_manager = LoginManager()
    #login_manager.login_view = 'auth.login'
    #login_manager.init_app(app)

    #@login_manager.user_loader
    #def load_user(user_id):
    #    return User.query.get(int(user_id))

    return app

def create_database(app):
    if not path.exists('Lab2Lab/' + DB_NAME):
        with app.app_context():
            db.create_all()
