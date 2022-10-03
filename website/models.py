from website import preferences
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class DBOverlay:
    def __init__(self) -> None:
        self.db = db

    def commit_to_db(self, obj):
        self.db.add(obj)
        self.db.commit()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    gender = db.Column(db.String(20))
    phone_number = db.Column(db.Integer)
    password = db.Column(db.String(150))
    age = db.Column(db.Integer)
    city = db.Column(db.String(50))


class Preferences(db.Model, UserMixin):
    userid = db.Column(db.Integer, primary_key=True)
    preferences = db.Column(db.Text)