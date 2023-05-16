from flask import Blueprint, redirect, request, flash, session
from flask_api import status
from flask.wrappers import Response
from database import dba, login_validation, extract_user_id


login_controller_blueprint = Blueprint("login_controller_blueprint", __name__)


@login_controller_blueprint.route("/api/login", methods = ["POST"])
def check_login():
     # Extract input data 
     email = request.form["email"]
     password = request.form["password"]

     # Return login answear for input data
     answear = login_validation(dba, email, password)

     # Check if user exists and proceed accordingly
     if answear:
          # Extract user id
          session["logged_in"] = True
          session["user_id"] = extract_user_id(dba, email)
          return redirect("/home", code=302)
     else:
          flash("login_error")
          return redirect("/login", code=302)
