from flask import Blueprint, make_response, jsonify, session, redirect
from flask_api import status
from flask.wrappers import Response
from database import dba


profile_controller_blueprint = Blueprint("profile_controller_blueprint", __name__)


@profile_controller_blueprint.route("/api/profile")
def profile() -> Response:
    return make_response(
        jsonify({"A": "a"}),
        status.HTTP_200_OK,
    )

