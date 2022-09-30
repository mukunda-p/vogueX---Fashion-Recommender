import functools

from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, session, url_for, request
)
from werkzeug.security import check_password_hash, generate_password_hash

recommendationsbp = Blueprint('recommendationsbp', __name__, url_prefix='/v1/')

'''
payload = {
    "occasion" : <occasion_name>
    "user_id" : <user_id>
}
'''


@recommendationsbp.route("/recommendations", methods=['POST'])
def get_recommendations():
    req_json_body = request.json
    recommendations = {
        "dress_list": [
            {
                "type" : "suit",
                "color" : "black"
            },
            {
                "type" : "one-piece",
                "color" : "yellow"
            }
        ]
    }
    
    x = jsonify(recommendations)
    return x
