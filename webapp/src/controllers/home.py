from flask import Blueprint, make_response, jsonify
from flask_api import status
from flask.wrappers import Response

home_controller_blueprint = Blueprint("home_controller_blueprint", __name__)


@home_controller_blueprint.route("/api/home")
def home() -> Response:
    return make_response(
        jsonify({"data": "random data", "text": "aaaaa", "number": 123, "a": None}),
        status.HTTP_200_OK,
    )
