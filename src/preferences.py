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

preferencesbp = Blueprint("preferences", __name__, url_prefix="/v1/")


@preferencesbp.route("/preferences", methods=["GET"])
def get_preferences():
    preferences = {
        "dress_preferences": [
            {
                "type": "suit",
            },
            {
                "type": "one-piece",
            },
            {
                "type": "flower-pattern-skirt",
            },
        ],
        "color_type": ["blue", "black", "yellow"],
    }

    x = jsonify(preferences)
    return x


@preferencesbp.route("/preferences", methods=["POST"])
def post_preferences():
    req = request.json

    x = jsonify({"status": 200})
    return x
