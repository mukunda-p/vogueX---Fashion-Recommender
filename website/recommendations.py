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

from . import contracts

from werkzeug.security import check_password_hash, generate_password_hash
from . import models

recommendationsbp = Blueprint("recommendationsbp", __name__, url_prefix="/")

"""
payload = {
    "occasion" : <occasion_name>
    "city" : <city>
}
"""


@recommendationsbp.route("/recommendations", methods=["POST"])
def get_recommendations():

    req_json_body = request.json
    city = ""
    occasion = ""
    # userid = '3'

    if contracts.SessionParameters.USERID not in session:
        return (
            jsonify(
                {
                    "error": "user not logged in",
                    "error_code": contracts.ErrorCodes.USER_NOT_LOGGED_IN,
                }
            ),
            403,
        )

    userid = session[contracts.SessionParameters.USERID]
    user = models.User.query.filter_by(id=int(userid)).first()
    if contracts.RecommendationContractRequest.CITY_KEY in req_json_body:
        city = req_json_body[contracts.RecommendationContractRequest.CITY_KEY]
    else:
        # take from the user table
        city = user.city

    if contracts.RecommendationContractRequest.OCCASION_KEY in req_json_body:
        occasion = req_json_body[contracts.RecommendationContractRequest.OCCASION_KEY]

    from . import helper

    help = helper.RecommendationHelper()
    links = help.giveRecommendations(userid, user.gender, occasion, city)

    recommendations = dict()
    recommendations[contracts.RecommendationContractResponse.LINKS] = []
    for link in links:
        recommendations[contracts.RecommendationContractResponse.LINKS].append(link)
    return jsonify(recommendations), 200
