from flask import Blueprint, make_response, jsonify
from flask_api import status
from flask.wrappers import Response

register_controller_blueprint = Blueprint("register_controller_blueprint", __name__)


@register_controller_blueprint.route("/register/api")
def register() -> Response:
    return make_response(
        jsonify({"data": "random data", "text": "aaaaa", "number": 123, "a": None}),
        status.HTTP_200_OK,
    )
    # verific logare
    return make_response(
        # se pot trimite date
        # status.HTTP_403_...
    )
