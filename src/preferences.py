
from flask import (
    Blueprint,
    jsonify,
    request,
)

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
    request.json

    x = jsonify({"status": 200})
    return x
