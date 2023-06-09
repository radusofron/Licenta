from controllers.itineraries import itineraries
from flask import Blueprint, make_response, render_template, session, redirect
from flask.wrappers import Response
from flask_api import status
import json


itineraries_view_blueprint = Blueprint("itineraries_view_blueprint", __name__)


@itineraries_view_blueprint.route("/itineraries")
def itineraries_view() -> Response:
    # User is not logged in
    if not session["logged_in"]:
        return make_response(
            redirect("/login", code=302)
        )
    
    # Extract data
    results = itineraries()
    itineraries_data = json.loads(results.data)
    option = itineraries_data["option"]
    
    # Case: no option given or wrong option
    if option == "redirect":
        return make_response(
            redirect("/home", code=302)
        )

    # Case: good option

    return make_response(
        render_template("itineraries.html", option = option)
    )