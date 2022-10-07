import functools

from flask import (
    Blueprint,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
    request,
)
from werkzeug.security import check_password_hash, generate_password_hash

dressbp = Blueprint("dress", __name__, url_prefix="/v1/")


@dressbp.route("/dresses", methods=["GET"])
def get_dresses():
    dresses = {
        "dress_list": [
            {"type": "suit", "color": "black"},
            {"type": "one-piece", "color": "yellow"},
        ]
    }

    x = jsonify(dresses)
    return x


@dressbp.route("/dresses", methods=["POST"])
def post_dresses():
    req = request.json

    x = jsonify({"status": 200})
    return x
