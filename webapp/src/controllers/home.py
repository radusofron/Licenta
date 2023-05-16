from flask import Blueprint, make_response, jsonify, session
from flask_api import status
from flask.wrappers import Response
from database import dba, extract_destinations_number, extract_wishlisted_destinations_number, extract_visited_destinations_number

home_controller_blueprint = Blueprint("home_controller_blueprint", __name__)


@home_controller_blueprint.route("/api/home")
def home() -> Response:
    # Extract total destinations number, wishlisted destinations number and visited destinations number
    total_destinations = extract_destinations_number(dba)
    wishlisted_destinations = extract_wishlisted_destinations_number(dba, session["user_id"])
    print("Aaaaaaaaaacum e :", wishlisted_destinations, type(wishlisted_destinations))
    visited_destinations = extract_visited_destinations_number(dba, session["user_id"])

    # Process total destinations number, wishlisted destinations number and visited destinations number
    if len(str(total_destinations)) == 1:
        total_destinations = "0" + str(total_destinations)
    if len(str(wishlisted_destinations)) == 1:
        wishlisted_destinations = "0" + str(wishlisted_destinations)
    if len(str(visited_destinations)) == 1:
        visited_destinations = "0" + str(visited_destinations)

    return make_response(
        jsonify({"total destinations": total_destinations, "wishlisted destinations": wishlisted_destinations, "visited destinations": visited_destinations}),
        status.HTTP_200_OK,
    )
