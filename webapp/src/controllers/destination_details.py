from flask import Blueprint, make_response, jsonify, session, request
from flask_api import status
from flask.wrappers import Response
from database import dba, extract_destinations_names
import requests


destination_details_controller_blueprint = Blueprint("destination_details_controller_blueprint", __name__)


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


def get_wiki_content(city: str):
    """Function extracts Wikipedia information for a given city
    """
    # Createa request
    response = requests.get("https://en.wikipedia.org/w/api.php?action=query&prop=extracts&titles=" + city + "&format=json")

    # Exit if request was not successfull
    if response.status_code != 200:
        return "";

    # Jsonify content
    json_content = response.json()

    # Parse the json in order to extract the content
    content = ""
    for id in json_content["query"]["pages"]:
        content = json_content["query"]["pages"][id]["extract"]
 
    return content


def get_statistics(city: str):
    """Function extracts statistics for a given city
    """
    pass


def get_reviews(city: str):
    """Function extracts reviews for a given city
    """
    pass


def get_weather(city: str):
    """Function extracts weather information for a given city
    """
    pass


@destination_details_controller_blueprint.route("/api/destination_details")
def destination_details() -> Response:
    # Check validation status
    option = validate_url_parameters()

    # Case: redirect
    if option == "redirect":
        return make_response(
            jsonify({"option": option}),
            status.HTTP_200_OK,
        )

    # Case: city exists
    # 1. Get Wikipedia content
    wikipedia = get_wiki_content(option)
    # 2. Create websites for photos links
    websites_links = []
    websites_links.append("https://www.pexels.com/search/" + option + "/")
    websites_links.append("https://unsplash.com/s/photos/" + option)
    # 3. Get statistics 
    # 4. Get reviews
    # 5. Get weather information
        
    return make_response(
        jsonify({"option": option, "wikipedia": wikipedia, "websites links": websites_links}),
        status.HTTP_200_OK,
    )