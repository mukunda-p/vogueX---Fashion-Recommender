import os
import tempfile
import pytest
from flask import Flask, g

# from website import create_app
from website.auth import db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

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
    return app

@pytest.fixture
def app():
    import pdb; pdb.set_trace()
    db_fd, db_path = tempfile.mkstemp()

    app = create_app()
    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()