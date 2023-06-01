from flask import Blueprint, make_response, jsonify, session, request
from flask_api import status
from flask.wrappers import Response
from database import dba, extract_destinations_names, extract_destination_id_by_name, extract_destination_average_grades, extract_destination_reviews
import requests
from datetime import datetime


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
    # Create request
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


def get_statistics_grades(city: str) -> dict:
    """Function extracts statistics for a given city
    """
    statistics = {"names": [], "grades": []}
    statistics["names"] = ["Attractions", "Accomodation", "Culture", "Entertainment", "Food and drink", 
              "History", "Natural beauty", "Night life", "Transport", "Safety"]
    statistics["grades"] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # Extract destination id
    destination_id = extract_destination_id_by_name(dba, city)
    
    # Case: wrong city
    if not destination_id:
        return statistics
    
    # City exists
    # Extract desitnation grades
    grades = extract_destination_average_grades(dba, destination_id)
    
    # Case: destination has no grades
    if not len(grades):
        return statistics
    
    # Create a list with floats
    float_grades = []

    # Grades exist
    # Convert Decimal to str then to float
    for index in range(10):
        float_grades.append(str(grades[0][index]))
        float_grades[index] = float(float_grades[index])
        float_grades[index] = round(float_grades[index], 1)

    # Update dictionary
    statistics["grades"] = float_grades

    return statistics


def change_date_format(date) -> str:
    """Function recieves a date and returns the time passed from that date untill now
    """
    current_date = datetime.now()

    # Different years
    if date.year < current_date.year:
        return str(current_date.year - date.year) + " year(s) ago"
    
    # Different months
    if date.month < current_date.year:
        return str(current_date.month - date.month) + " month(s) ago"
    
    # Different days
    if date.day < current_date.day:
        return str(current_date.day - date.day) + " day(s) ago"

    # Different hours
    if date.hour < current_date.day:
        return str(current_date.hour - date.hour) + " hour(s) ago"
    
    # Different minutes
    if date.minute < current_date.minute:
        return str(current_date.minute - date.minute) + " minute(s) ago"
    
    return "Now"
        

def get_reviews_and_associated_data(city: str) -> dict:
    """Function extracts reviews for a given city
    """
    # Extract destination id
    destination_id = extract_destination_id_by_name(dba, city)

    # Case: wrong city
    if not destination_id:
        return dict()
    
    # City exists
    # Extract desitnation grades
    reviews_rows = extract_destination_reviews(dba, destination_id)

    # Case: destination has no reviews
    if not len(reviews_rows):
        return dict()
    
    # Create dictionary
    reviews = {"username": [], "photo_name": [], "review": [], "date": []}
    for row in reviews_rows:
        reviews["username"].append(str(row[0]))
        reviews["photo_name"].append(row[1])
        reviews["review"].append(str(row[2]))
        reviews["date"].append(row[3])

    # If user has no photo change photo_name to 0, otherwise transform to string
    for index in range(len(reviews["photo_name"])):
        if reviews["photo_name"][index] is None:
            reviews["photo_name"][index] = "0"
        else:
            reviews["photo_name"][index] = str(reviews["photo_name"][index])

    # Change date format
    for index in range(len(reviews["date"])):
        reviews["date"][index] = change_date_format(reviews["date"][index])
    
    return reviews


def get_weather_details(city: str) -> dict:
    """Function extracts weather information for a given city
    """
    return dict()


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
    statistics = get_statistics_grades(option)

    # 4. Get reviews
    reviews = get_reviews_and_associated_data(option)
    
    # 5. Get weather information
    weather = get_weather_details(option)
        
    return make_response(
        jsonify({"option": option, "wikipedia": wikipedia, "websites links": websites_links, "statistics": statistics, "reviews": reviews}),
        status.HTTP_200_OK,
    )