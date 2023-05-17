from flask import Blueprint, make_response, jsonify, session, redirect
from flask_api import status
from flask.wrappers import Response
from database import dba, extract_destinations_number, extract_wishlisted_destinations_number, extract_visited_destinations_number


home_controller_blueprint = Blueprint("home_controller_blueprint", __name__)


def process_destinations_number(destinations_number: str) -> str:
    """Function adds a 0 in front of 1 digit strings
    """
    if len(destinations_number) == 1:
        destinations_number = "0" + destinations_number
    return destinations_number


@home_controller_blueprint.route("/api/home")
def home() -> Response:
    # Extract total destinations, wishlisted destinations and visited destinations
    total_destinations = extract_destinations_number(dba)
    wishlisted_destinations = extract_wishlisted_destinations_number(dba, session["user_id"])
    visited_destinations = extract_visited_destinations_number(dba, session["user_id"])

    # Process total destinations number, wishlisted destinations number and visited destinations number
    total_destinations = process_destinations_number(str(total_destinations))
    wishlisted_destinations = process_destinations_number(str(wishlisted_destinations))
    visited_destinations = process_destinations_number(str(visited_destinations))

    return make_response(
        jsonify({"total destinations": total_destinations, "wishlisted destinations": wishlisted_destinations, "visited destinations": visited_destinations}),
        status.HTTP_200_OK,
    )
