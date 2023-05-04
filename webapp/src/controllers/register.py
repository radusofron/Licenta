from flask import Blueprint, make_response, jsonify, redirect, request
from flask_api import status
from flask.wrappers import Response
from database import dba, extract_user_username, extract_user_email


register_controller_blueprint = Blueprint("register_controller_blueprint", __name__)


@register_controller_blueprint.route("/api/register", methods = ["POST"])
def try_to_register():

    # Extract input data
    username = request.form["username"] 
    email = request.form["email"]
    password = request.form["password"]
    password_confirmation = request.form["password-confirmation"]

    # Try to return input username from database
    username_rows = extract_user_username(dba, username)
    # Try to return input email from database
    email_rows = extract_user_email(dba, email)

    # Check if account can be created and proceed accordingly 
    # (Password validation was made via Javascript)
    if len(username_rows) == 0:
        if len(email_rows) == 0:
            # TODO -> inserez in baza de date
            return redirect("/home", code=302)
        else:
            # TODO -> returnez motiv email coincide altui cont
            return redirect("/login", code=302)
    else:
        if len(email_rows) == 0:
            # TODO -> returnez motiv username coincide altui cont
            return redirect("/login", code=302)
        else:
            # TODO -> returnez motiv username & email coincid altui cont
            return redirect("/login", code=302)