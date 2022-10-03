import functools
import json
import re
from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, session, url_for, request
)
from werkzeug.security import check_password_hash, generate_password_hash

from website import contracts
from . import models
from . import db 
preferencesbp = Blueprint('preferences', __name__, url_prefix='/')

@preferencesbp.route("/default-preferences", methods = ["GET"])
def get_default_preferences():
    if contracts.SessionParameters.USERID not in session:
        return jsonify({"error": "user not logged in", "error_code": contracts.ErrorCodes.USER_NOT_LOGGED_IN }), 403
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
        "preferences" : {
        "formal" :  [{
                "type" : "suit",
                "color" : "black",
                
            }],
        "beach" : [
            {
                "type" : "tshirt",
                "color" : "blue",
            }],
        "date" :[
            {
                "type" : "shirt",
                "color" : "navy-blue",
            }]
        }
    }

    if contracts.SessionParameters.USERID not in session:
        return jsonify({"error": "user not logged in", "error_code": contracts.ErrorCodes.USER_NOT_LOGGED_IN }), 403
    ### query the preferences table and check if preferences have been saved or not
    userid = session[contracts.SessionParameters.USERID]
    import pdb; pdb.set_trace()
    preferencesObj = models.Preference.query.filter_by(userid = int(userid)).first()
    if not preferencesObj:
        return jsonify({"error_code" : contracts.ErrorCodes.OBJECT_NOT_SAVED, "error" : "preferences not saved"}), 400

    userpreferences = preferencesObj.preferences
    response = json.loads(userpreferences)
    return jsonify(response), 200

'''
Request : 

{
    "preferences" : {
    "formal" :  [{
            "type" : "suit",
            "color" : "black",
            
        }],
    "beach" : [
        {
            "type" : "tshirt",
            "color" : "blue",
        }],
    "date" :[
        {
            "type" : "shirt",
            "color" : "navy-blue",
        }]
    }
}

Response : 
{
    "status_code" : 200,
}

'''


@preferencesbp.route("/preferences", methods=['POST'])
def post_preferences():
    req = request.json

    if contracts.SessionParameters.USERID not in session:
        return jsonify({"error": "user not logged in", "error_code": contracts.ErrorCodes.USER_NOT_LOGGED_IN }), 403

    userid = session['userid']

    user_preferences = "{}"

    if contracts.PreferenceContractRequest.PREFERENCES in req:
        user_preferences = req[contracts.PreferenceContractRequest.PREFERENCES]

    preferenceObject = models.Preference.query.filter_by(userid = int(userid)).first()
    if not preferenceObject:
        # create a new one
        preferenceObject = models.Preference(userid=int(userid), preferences = json.dumps(user_preferences))
    db.session.add(preferenceObject)
    db.session.commit()

    return jsonify({"status" : 200}), 200
