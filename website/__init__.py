from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"
db_overlay = None

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://fashion:fashion@localhost/fashion'

    db.init_app(app)

    from .views import views
    from .auth import auth

    from . import preferences
    from . import recommendations

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(preferences.preferencesbp)
    app.register_blueprint(recommendations.recommendationsbp)

    from .models import User  

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
