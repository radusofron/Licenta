from flask import Blueprint, make_response, jsonify
from flask_api import status
from flask.wrappers import Response

login_controller_blueprint = Blueprint("login_controller_blueprint", __name__)


@login_controller_blueprint.route("/login/api")
def login() -> Response:
    return make_response(
        jsonify({"data": "random data", "text": "aaaaa", "number": 123, "a": None}),
        status.HTTP_200_OK,
    )
    # verific logare
    return make_response(
        # se pot trimite date
        # status.HTTP_403_...
    )
