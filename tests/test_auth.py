from flask import Flask
import json
from website.auth import auth
from website.auth import db




def test_login_get():
    app = Flask(__name__)
    app.register_blueprint(auth)
    client = app.test_client()
    url = "/login"

    response = client.get(url)
    print(response.get_data())
    assert response.status_code == 200


#  TODO: The below test case does successfuly post a request but it errors out when fetching from DB. resolve this
def test_login_post():
    app = Flask(__name__)
    app.register_blueprint(auth)
    
    client = app.test_client()
    mimetype = 'application/x-www-form-urlencoded'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'email': 'soccerwolves11@gmail.com',
        'password': 'qqqqqqq'
    }
    url = "/login"

    response = client.post(url, data=data, headers=headers)
    assert response.status_code == 200