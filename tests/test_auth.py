from flask import Flask, g
import json
from website.auth import auth
from website.auth import db
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import sys
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
   
def test_login_get():
    app = create_app()
    client = app.test_client()
    url = "/login"

    response = client.get(url)
    print(response.get_data())
    assert response.status_code == 200


#  TODO: The below test case does successfuly post a request but it errors out when fetching from DB. resolve this
def test_login_post():
    app = create_app()

    client = app.test_client()
    mimetype = 'application/x-www-form-urlencoded'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    # This user is not present in the db
    data = {
        'email': 'test@gmail.com',
        'password': 'password123'
    }
    url = "/login"

    response = client.post(url, data=data, headers=headers)
    assert response.status_code == 200