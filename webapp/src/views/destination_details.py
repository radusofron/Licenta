from controllers.destination_details import destination_details
from flask import Blueprint, make_response, render_template, session, redirect
from flask.wrappers import Response
from flask_api import status
import json


destination_details_view_blueprint = Blueprint("destination_details_view_blueprint", __name__)


def get_reviews_filter_options():
    """Function returns filter options for reviews
    """
    filter_options = {"Traveler level": {"options": ["Highest to lowest", "Lowest to highest"], "name": "level", "ids": ["highest", "lowest"]},
                      "Overall feeling": {"options": ["Best to worst", "Worst to best"], "name":"feeling", "ids": ["best", "worst"]},
                      "Date": {"options": ["Descending", "Ascending"], "name": "date", "ids": ["descending", "ascending"]}
                      }
    return filter_options


@destination_details_view_blueprint.route("/destination")
def destination_details_view() -> Response:
    # User is not logged in
    if not session["logged_in"]:
        return make_response(
            redirect("/login", code=302)
        )
    
    # Extract data
    results = destination_details()
    destination_data = json.loads(results.data)
    option = destination_data["option"]
    
    # Case: no option given or wrong option
    if option == "redirect":
        return make_response(
            redirect("/destinations?option=all", code=302)
        )

    # Case: good option
    city_status = destination_data["city status"]
    touristic_objectives = destination_data["touristic objectives"]
    wikipedia = destination_data["wikipedia"]
    websites_links = destination_data["websites links"]
    statistics = destination_data["statistics"]
    reviews_filters = get_reviews_filter_options()
    reviews = destination_data["reviews"]
    weather_data = destination_data["weather data"]

    return make_response(
        render_template("destination_details.html", city_name = option, city_status = city_status, touristic_objectives = touristic_objectives, 
                        wikipedia = wikipedia, websites_links = websites_links, statistics = statistics, reviews_filters = reviews_filters,
                        reviews = reviews, weather_data = weather_data)
    )