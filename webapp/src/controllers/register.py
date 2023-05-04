from flask import Blueprint, make_response, jsonify, redirect, request, flash
from flask_api import status
from flask.wrappers import Response
from database import dba, extract_user_username, extract_user_email


register_controller_blueprint = Blueprint("register_controller_blueprint", __name__)


@register_controller_blueprint.route("/api/register", methods = ["POST"])
def register():
    
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
    if len(username_rows) == 1:
        flash("Username already exists!")
        return redirect("/register", code=302)
    if len(email_rows) == 1:
        flash("Email already exists!")
        return redirect("/register", code=302)
    if len(password) < 8:
        flash("Password too short!")
        return redirect("/register", code=302)
    if password != password_confirmation:
        flash("Passwords are different!")
        return redirect("/register", code=302)

    # TODO -> inserez in baza de date
    return redirect("/home", code=302)
       