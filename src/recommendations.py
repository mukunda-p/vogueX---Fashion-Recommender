import functools
import contracts
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

recommendationsbp = Blueprint("recommendationsbp", __name__, url_prefix="/v1/")

"""
payload = {
    "occasion" : <occasion_name>
    "user_id" : <user_id>
}
"""


@recommendationsbp.route("/recommendations", methods=["POST"])
def get_recommendations():
    req_json_body = request.json

    city = None
    occasion = None
    if contracts.RecommendationContractRequest.CITY_KEY in req_json_body:
        city = req_json_body[contracts.RecommendationContractRequest.CITY_KEY]

    if contracts.RecommendationContractRequest.OCCASION_KEY in req_json_body:
        occasion = req_json_body[contracts.RecommendationContractRequest.OCCASION_KEY]

    import helper

    help = helper.RecommendationHelper()
    links = help.giveRecommendations(occasion, city)

    recommendations = dict()
    recommendations[contracts.RecommendationContractResponse.LINKS] = []
    for link in links:
        recommendations[contracts.RecommendationContractResponse.LINKS].append(link)
    return jsonify(recommendations), 200
