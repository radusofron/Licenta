from flask import Blueprint, redirect, request, flash, session
from flask_api import status
from flask.wrappers import Response
from database import dba, extract_username, extract_email, insert_user, extract_user_id


register_controller_blueprint = Blueprint("register_controller_blueprint", __name__)


@register_controller_blueprint.route("/api/register", methods = ["POST"])
def register():
    
    # Extract input data
    username = request.form["username"] 
    email = request.form["email"]
    password = request.form["password"]
    password_confirmation = request.form["password-confirmation"]

    # Try to return input username from database
    username_rows = extract_username(dba, username)
    # Try to return input email from database
    email_rows = extract_email(dba, email)

    # Check if account can be created and proceed accordingly
    if len(username_rows) == 1:
        flash("username_error")
        return redirect("/register", code=302)
    if len(email_rows) == 1:
        flash("email_error")
        return redirect("/register", code=302)
    if len(password) < 8:
        flash("password_error")
        return redirect("/register", code=302)
    if password != password_confirmation:
        flash("passwords_error")
        return redirect("/register", code=302)

    # Check finished
    insert_user(dba, username, email, password)
    session["logged_in"] = True
    session["user_id"] = extract_user_id(dba, email)
    return redirect("/home", code=302)
       