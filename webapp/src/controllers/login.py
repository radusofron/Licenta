from flask import Blueprint, make_response, jsonify, redirect, request
from flask_api import status
from flask.wrappers import Response

login_controller_blueprint = Blueprint("login_controller_blueprint", __name__)


@login_controller_blueprint.route("/api/login", methods = ["POST"])
def check_login():
     email = request.form["email"]
     password = request.form["password"]
     print("email:", email)
     print("password:", password)
     return redirect("/home", code=302)
