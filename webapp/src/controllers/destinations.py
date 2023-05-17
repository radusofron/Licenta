from flask import Blueprint, make_response, jsonify, session, request
from flask_api import status
from flask.wrappers import Response
from database import dba


destinations_controller_blueprint = Blueprint("destinations_controller_blueprint", __name__)


@destinations_controller_blueprint.route("/api/destinations")
def destinations() -> Response:
    # Extract option
    option = request.args.get("option")

    # Case: no option given or wrong option
    if option is None or option not in ["visited", "wishlisted", "all"]:
        option = "redirect"

    # Case: visited

    
    return make_response(
        jsonify({"option": option}),
        status.HTTP_200_OK,
    )