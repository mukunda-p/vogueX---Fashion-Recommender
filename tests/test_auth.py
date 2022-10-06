from flask import Flask, g
import json
from website.auth import auth
from website.auth import db
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import sys
sys.path.append("..")
   
def test_login_get(app):
    app = app()
    client = app.test_client()
    url = "/login"

    response = client.get(url)
    print(response.get_data())
    assert response.status_code == 200


#  TODO: The below test case does successfuly post a request but it errors out when fetching from DB. resolve this
def test_login_post(app):
    app = app()

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