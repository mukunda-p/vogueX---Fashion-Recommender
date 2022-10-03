import functools

from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, session, url_for, request
)
from werkzeug.security import check_password_hash, generate_password_hash

from website import contracts
from . import models
from . import db_overlay
preferencesbp = Blueprint('preferences', __name__, url_prefix='/')

@preferencesbp.route("/default-preferences", methods = ["GET"])
def get_default_preferences():
    default_preferences = {
        "male" : {
            "preferences" : [
                    {
                        "type" : "suit",
                        "color" : "black",
                        "occasion" : "formal"
                    },
                    {
                        "type" : "tshirt",
                        "color" : "blue",
                        "occasion" : "beach"
                    },
                    {
                        "type" : "shirt",
                        "color" : "navy-blue",
                        "occasion" : "office"
                    }
                ]
        },

        "female" : {
            "preferences" : [
                    {
                        "type" : "suit",
                        "color" : "black",
                        "occasion" : "formal"
                    },
                    {
                        "type" : "top",
                        "color" : "blue",
                        "occasion" : "beach"
                    },
                    {
                        "type" : "shirt",
                        "color" : "navy-blue",
                        "occasion" : "office"
                    },
                    {
                        "type": "floral-skirt",
                        "color" : "black",
                        "occasion" : "date"
                    }
                ]
        }


    }
    return jsonify(default_preferences)

@preferencesbp.route("/preferences", methods=['GET'])
def get_preferences():
    '''
    response : 

    {
        "
    }

    '''
    preferences = {
        "dress_preferences": [
            {
                "type" : "suit",
            },
            {
                "type" : "one-piece",
            },
            {
                "type" : "flower-pattern-skirt",
            }
        ],

        "color_type" : [
            'blue', 'black', 'yellow'
        ]
    }

    if contracts.SessionParameters.USERID not in session:
        return {}, 403

    ### query the preferences table and check if preferences have been saved or not
    userid = session[contracts.SessionParameters.USERID]
    import pdb; pdb.set_trace()
    preferencesObj = models.Preferences.query_filter(userid = userid).first()
    if not preferencesObj:
        return jsonify({"error_code" : 2, "error" : "preferences not saved"}), 400
    
    x = jsonify(preferences)
    return x

'''
Request : 

{
    "preferences" : [
        {
            "type" : "suit",
            "color" : "black",
            "occasion" : "formal"
        },
        {
            "type" : "tshirt",
            "color" : "blue",
            "occasion" : "beach"
        },
        {
            "type" : "shirt",
            "color" : "navy-blue",
            "occasion" : "
        }
    ]
}

Response : 
{
    "status_code" : 200,
}

'''


@preferencesbp.route("/preferences", methods=['POST'])
def post_preferences():
    req = request.json
    userid = session['userid']
    preferenceObject = models.Preferences.query.filter_by(userid = userid).first()

    if not preferenceObject:
        # create a new one
        preferenceObject = models.Preferences()

    # check if the preferences exist for the customer already
    for pref in req['preferences']:
        pass
    
    db_overlay.commit_to_db(preferenceObject)
    x = jsonify({"status" : 200})
    return x
