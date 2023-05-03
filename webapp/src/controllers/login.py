from flask import Blueprint, make_response, jsonify, redirect, request
from flask_api import status
from flask.wrappers import Response
from database import dba, extract_user


login_controller_blueprint = Blueprint("login_controller_blueprint", __name__)


@login_controller_blueprint.route("/api/login", methods = ["POST"])
def check_login():

     # Extract input data 
     email = request.form["email"]
     password = request.form["password"]

     # Return correspondent user for input data from database
     rows = extract_user(dba, email, password)

     # Check if user exists and proceed accordingly
     if len(rows) == 1:
          return redirect("/home", code=302)
     else:
          return redirect("/login", code=302)  # TODO -> returnez problema aparuta
