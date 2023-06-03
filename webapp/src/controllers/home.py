from flask import Blueprint, make_response, jsonify, session
from flask_api import status
from flask.wrappers import Response
from database import dba, extract_destinations_number, extract_wishlisted_destinations_number, extract_visited_destinations_number, extract_visited_destinations_names, extract_wishlisted_destinations_names


home_controller_blueprint = Blueprint("home_controller_blueprint", __name__)


def create_list_with_destinations(destinations: list) -> list:
    """Function creates a list containing all the correspondent destinations names

    Database's function returns a list with tuples containing the names.

    This function returns a list containing the names. It returns an empty list if no destination was found.

    Parameters:
        destinations: a list with tuples containing the names

    Returns:
        a list as described above
    """
    new_destinations_list = []

    # Parse the list with the tuples and add the names in a new list
    if len(destinations):
        for tpl in destinations:
            new_destinations_list.append(tpl[0])

    return new_destinations_list


def store_visited_destinations_names():
    """This function stores the destinations marked as visited in the session.
    """
    visited_destinations_names = extract_visited_destinations_names(dba, session["user_id"])
    visited_destinations_names = create_list_with_destinations(visited_destinations_names)
    session["visited_destinations"] = visited_destinations_names


def store_wishlisted_destinations_names():
    """This function stores the destinations added to wishlist in the session.
    """
    wishlisted_destinations_names = extract_wishlisted_destinations_names(dba, session["user_id"])
    wishlisted_destinations_names = create_list_with_destinations(wishlisted_destinations_names)
    session["wishlisted_destinations"] = wishlisted_destinations_names


@home_controller_blueprint.route("/api/home")
def home() -> Response:
    # Extract total destinations, wishlisted destinations and visited destinations
    total_destinations = extract_destinations_number(dba)
    wishlisted_destinations = extract_wishlisted_destinations_number(dba, session["user_id"])
    visited_destinations = extract_visited_destinations_number(dba, session["user_id"])

    # Modify number format
    total_destinations = (str(total_destinations)).zfill(2)
    wishlisted_destinations = (str(wishlisted_destinations)).zfill(2)
    visited_destinations = (str(visited_destinations)).zfill(2)

    # Store in the session visited destinations and destinations added on wishlist
    store_visited_destinations_names()
    store_wishlisted_destinations_names()

    return make_response(
        jsonify({"total destinations": total_destinations, "wishlisted destinations": wishlisted_destinations, "visited destinations": visited_destinations}),
        status.HTTP_200_OK,
    )
