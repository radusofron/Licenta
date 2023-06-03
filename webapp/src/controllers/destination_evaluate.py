from flask import Blueprint, make_response, jsonify, session, request, redirect, flash, get_flashed_messages
from flask_api import status
from flask.wrappers import Response
from database import dba, extract_destinations_names, extract_visited_destination_date_for_user
from datetime import datetime


destination_evaluate_controller_blueprint = Blueprint("destination_controller_blueprint", __name__)


def create_list_with_destinations(destinations: list) -> list:
    """Function creates a list containing all the destinations names

    Database's function returns a list with tuples containing the names 

    This function returns a list containing the names
    """
    list_with_destiantions = []

    # Parse the list with the tuples and add the names in a new list
    if len(destinations):
        for tpl in destinations:
            list_with_destiantions.append(tpl[0])

    return list_with_destiantions


def validate_url_parameters():
    """Function validates url parameters. All possible cases included
    """
    # Extract city
    city = request.args.get("city")

    # Extract available destinations 
    destinations = extract_destinations_names(dba)
    destinations = create_list_with_destinations(destinations)

    # Case: no city given
    if city is None:
        action = "redirect"
        return action
    
    # Transform city to start with capital letter then lowercase letters
    city = str(city).capitalize()

    # Case: wrong city
    if city not in destinations:
        action = "redirect"
        return action
    
    # City exists
    action = city

    return action


def get_visited_date(city: str):
    """Function extracts and processes the date when the destination was marked as visited by the user
    """
    visited_date = extract_visited_destination_date_for_user(dba, session["user_id"], city)
    visited_date = visited_date.strftime('%d %b %Y')  # type: ignore
    return visited_date


def get_evaluation_aspects() -> list[str]:
    """Function extracts evaluation aspects
    """
    aspects = ["Attractions", "Accomodation", "Culture", "Entertainment", "Food and drink", 
              "History", "Natural beauty", "Night life", "Transport", "Safety"]
    return aspects


@destination_evaluate_controller_blueprint.route("/api/evaluate", methods=['GET', 'POST'])
def destination_evaluate() -> Response:
    # POST request:
    if request.method == "POST":

        # Identify form

        return make_response(
            redirect("/evaluate?city=" + session["current_city"], code=302)
        )

    # GET request:

    # Check validation status
    option = validate_url_parameters()

    # Case: redirect
    if option == "redirect":
        return make_response(
            jsonify({"option": option}),
            status.HTTP_200_OK,
        )

    # Case: city exists

    # Save city in session
    session["current_city"] = option

    # 1. Get visited destination date
    visited_date = get_visited_date(option)

    # 2. Get evaluation content
    aspects = get_evaluation_aspects()
        
    return make_response(
        jsonify({"option": option, "visited date": visited_date, "aspects": aspects}),
        status.HTTP_200_OK,
    )