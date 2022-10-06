from urllib import response
from flask import Flask, g
import json
from website.auth import auth
from website.auth import db
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import sys
from website.models import User
sys.path.append("..")

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://fashion:fashion@localhost/fashion_test'

    db.init_app(app)

    import website.views
    import website.auth

    # from .. import preferences
    import website.preferences
    import website.recommendations
    # from . import recommendations

    app.register_blueprint(website.views.views, url_prefix='/')
    app.register_blueprint(website.auth.auth, url_prefix='/')
    app.register_blueprint(website.preferences.preferencesbp)
    app.register_blueprint(website.recommendations.recommendationsbp)

    import website.models

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return website.models.User.query.get(int(id))

    return app


def test_recommendations():
    app = create_app()
    client = app.test_client()

    data = json.dumps({'occasion': 'birthday', 'city': 'Raleigh'})
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype
        # 'Accept': mimetype
    }

    url = "/recommendations"
    with client as c:
        var = c.post(url, data=data, headers=headers)
        assert var.status_code == 403

#### [WIP] trying to mock DB
def test_recommendations_with_session():
    app = create_app()
    client = app.test_client()

    data = json.dumps({'occasion': 'birthday', 'city': 'Raleigh'})
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype
        # 'Accept': mimetype
    }

    user = User()
    user.id = 1

    url = "/recommendations"
    with client as c:
        with c.session_transaction() as sess:
            sess['userid'] = 1
        
        var = c.post(url, data=data, headers=headers)
        assert var.status_code == 200