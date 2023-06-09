from flask import Blueprint, make_response, jsonify, session, request
from flask_api import status
from flask.wrappers import Response
from database import dba, extract_itineraries_id, extract_itineraries_main_details, extract_destination_name_by_id

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
    itineraries_ids = extract_itineraries_id(dba, session["user_id"])
    itineraries_ids = create_list_with_itineraries(itineraries_ids)

    # Case: no paramater given
    if option is None:
        action = "redirect"
        return action
    
    # Add parameter all as a valid option
    itineraries_ids.append("all")

    # Case: wrong itinerary id
    if option not in itineraries_ids:
        action = "redirect"
        return action
    
    # Parameter exists
    return option


def get_itineraries():
    """Function extracts and processes all the travel itineraries of an user
    """
    # Extarct itineraries main details
    itineraries = extract_itineraries_main_details(dba, session["user_id"])

    # Modify the existing itineraries:
    # 1. Add city name
    # 2. If an itinerary has no name, set its id as the name
    # 3. Convert date to string format
    formatted_itineraries = []
    for itinerary in itineraries:
        destination_name = extract_destination_name_by_id(dba, itinerary[2]) # type: ignore
        if itinerary[1] == "":
            formatted_itinerary = (itinerary[0], destination_name, itinerary[3].strftime('%d %b %Y at %H:%M:%S')) #type: ignore
        else:
            formatted_itinerary = (itinerary[1], destination_name, itinerary[3].strftime('%d %b %Y at %H:%M:%S')) #type: ignore
        formatted_itineraries.append(formatted_itinerary)

    return formatted_itineraries
            
    
@itineraries_controller_blueprint.route("/api/itineraries")
def itineraries_details() -> Response:

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
    if option == "all":
        itineraries = get_itineraries()
        return make_response(
            jsonify({"option": option, "itineraries": itineraries}),
            status.HTTP_200_OK,
        )
    
    # Case: specific itinerary
    return make_response(
        jsonify({"option": option}),
        status.HTTP_200_OK,
    )