from flask import Blueprint, make_response, jsonify, session, request
from flask_api import status
from flask.wrappers import Response
from database import dba, extract_visited_destinations_names, extract_wishlisted_destinations_names, extract_most_visited_destinations_names, extract_most_reviewed_destinations_names, extract_destinations_names


destinations_controller_blueprint = Blueprint("destinations_controller_blueprint", __name__)


def create_specific_destinations(destinations: list):
    """Function creates a list containing all the destinations names

    Database's function returns a list with tuples containing the names.

    This function returns a list containing the names. It returns an empty list if no destination was found.
    """
    specific_destinations = []

    # Parse the list with the tuples and add the names in a new list
    if len(destinations):
        for tpl in destinations:
            specific_destinations.append(tpl[0])

    return specific_destinations


@destinations_controller_blueprint.route("/api/destinations")
def destinations() -> Response:
    # Extract option
    option = request.args.get("option")

    # List to store specific destinations (based on option chosen: visited / wishlisted / most visited and most reviewed)
    specific_destinations = []

    # Case: no option given or wrong option
    if option is None or option not in ["visited", "wishlisted", "all"]:
        option = "redirect"
    
    # Case: visited
    elif option == "visited":
        visited_destinations = extract_visited_destinations_names(dba, session["user_id"])
        specific_destinations = create_specific_destinations(visited_destinations)
        
    
    # Case: wishlisted
    elif option == "wishlisted":
        wishlisted_destinations = extract_wishlisted_destinations_names(dba, session["user_id"])
        specific_destinations = create_specific_destinations(wishlisted_destinations)

    # Case: most visited and most reviewed
    else:
        most_visited_destinations = extract_most_visited_destinations_names(dba)
        specific_destinations = create_specific_destinations(most_visited_destinations)
        # Add a delimiter
        specific_destinations.append(" ")
        # Add to the same list
        most_reviewed_destinations = extract_most_reviewed_destinations_names(dba)
        specific_destinations.extend(create_specific_destinations(most_reviewed_destinations))

    # Common for all cases
    destinations = extract_destinations_names(dba)
    destinations = create_specific_destinations(destinations)
    
    return make_response(
        jsonify({"option": option, "specific destinations": specific_destinations, "all destinations": destinations}),
        status.HTTP_200_OK,
    )