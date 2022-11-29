from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    jsonify,
    redirect,
    url_for,
    session,
)

from flask_login import login_required, current_user
from . import models
from . import db
from . import contracts
from .models import Favourite
import json

favouritesbp = Blueprint("favourites", __name__)


@favouritesbp.route("/favourites", methods=["POST", "GET", "PUT"])
# @login_required
def post_favourites():
    req_json_body = request.json

    favourite_url = ""
    search_occasion = ""
    search_weather = ""

    userid = '1'

    # if contracts.SessionParameters.USERID not in session:
    #     return (
    #         jsonify(
    #             {
    #                 "error": "user not logged in",
    #                 "error_code": contracts.ErrorCodes.USER_NOT_LOGGED_IN,
    #             }
    #         ),
    #         403,
    #     )

    if contracts.FavouritesContrastRequest.FAVOURITE_URL_KEY in req_json_body:
        favourite_url = req_json_body[contracts.FavouritesContrastRequest.FAVOURITE_URL_KEY]

    if contracts.FavouritesContrastRequest.SEARCH_OCCASION_KEY in req_json_body:
        search_occasion = req_json_body[contracts.FavouritesContrastRequest.SEARCH_OCCASION_KEY]

    if contracts.FavouritesContrastRequest.SEARCH_WEATHER_KEY in req_json_body:
        search_weather = req_json_body[contracts.FavouritesContrastRequest.SEARCH_WEATHER_KEY]

    # For the post request.
    if request.method == "POST":

        new_favourite = Favourite(
            userid=userid,
            favourite_url=favourite_url,
            search_occasion=search_occasion,
            search_weather=search_weather
        )

        db.session.add(new_favourite)
        db.session.commit()

        return "Adding favourite success"

    elif request.method == "GET":
        favourite_query = Favourite.query.filter_by(userid=int(userid))
        # print(favourite_list)
        if favourite_url != "":
            favourite_query = favourite_query.filter_by(favourite_url=favourite_url)
        if search_occasion != "":
            favourite_query = favourite_query.filter_by(search_occasion=search_occasion)
        if search_weather != "":
            favourite_query = favourite_query.filter_by(search_weather=search_weather)

        favourite_resp = favourite_query.all()
        # print(favourite_list[0])

        sorted_fav_list = {}

        for row in favourite_resp:
            fav = json.loads(json.dumps(Favourite.serialize(row)))

            if fav["search_occasion"] in sorted_fav_list.keys():
                curr_list = list(sorted_fav_list[fav["search_occasion"]])
                curr_list.append(fav)
                sorted_fav_list[fav["search_occasion"]] = curr_list
            else:
                sorted_fav_list[fav["search_occasion"]] = [fav]  
                    

        return sorted_fav_list

    else:
        favourite_query = Favourite.query.filter_by(userid=int(userid))
        # print(favourite_list)
        if favourite_url != "":
            favourite_query = favourite_query.filter_by(favourite_url=favourite_url)
        if search_occasion != "":
            favourite_query = favourite_query.filter_by(search_occasion=search_occasion)
        if search_weather != "":
            favourite_query = favourite_query.filter_by(search_weather=search_weather)

        favourite_resp = favourite_query.all()
        for row in favourite_resp:
            db.session.delete(row)
        db.session.commit()

        return "Delete Success"
