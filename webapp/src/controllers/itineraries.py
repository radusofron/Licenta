from flask import Blueprint, make_response, jsonify, session, request
from flask_api import status
from flask.wrappers import Response
from database import dba, extract_itineraries_names

itineraries_controller_blueprint = Blueprint("itineraries_controller_blueprint", __name__)

def create_list_with_itineraries(itineraries: list) -> list:
    """Function creates a list containing all the destinations names

    Database's function returns a list with tuples containing the names 

    This function returns a list containing the names
    """
    list_with_itineraries = []

    # Parse the list with the tuples and add the names in a new list
    if len(itineraries):
        for tpl in itineraries:
            list_with_itineraries.append(tpl[0])

    return list_with_itineraries


def validate_url_parameters():
    """Function validates url parameters. All possible cases included
    """
    # Extract parameter
    option = request.args.get("id")

    # Extract user's itineraries
    itineraries_names = extract_itineraries_names(dba, session["user_id"])
    itineraries_names = create_list_with_itineraries(itineraries_names)

    # Case: no paramater given
    if option is None:
        action = "redirect"
        return action
    
    # Add parameter all as a valid option
    itineraries_names.append("all")

    # Case: wrong itinerary id
    if option not in itineraries_names:
        action = "redirect"
        return action
    
    # Parameter exists
    return option


@itineraries_controller_blueprint.route("/api/itineraries")
def itineraries() -> Response:

    # GET request:

    # Check validation status
    option = validate_url_parameters()

    # Case: redirect
    if option == "redirect":
        return make_response(
            jsonify({"option": option}),
            status.HTTP_200_OK,
        )
    
    # Case: all itineraries
    
    # Case: itinerary exists

    return make_response(
        jsonify({"option": option}),
        status.HTTP_200_OK,
    )