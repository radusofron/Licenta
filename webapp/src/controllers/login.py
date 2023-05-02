from flask import Blueprint, make_response, jsonify, request
from flask_api import status
from flask.wrappers import Response

login_controller_blueprint = Blueprint("login_controller_blueprint", __name__)


@login_controller_blueprint.route("/login/api")
def login() -> Response:
    username = request.form["Username"]
    print(username)
    print("Hello")
    return make_response(
        status.HTTP_200_OK,
    )
    # return make_response(
    #     # se pot trimite date
    #     # status.HTTP_403_...
    # )
