from controllers.destinations import destinations
from flask import Blueprint, make_response, render_template, session, redirect
from flask.wrappers import Response
from flask_api import status
import json


destinations_view_blueprint = Blueprint("destinations_view_blueprint", __name__)


@destinations_view_blueprint.route("/destinations")
def destinations_view() -> Response:
    if session["logged_in"]:
        # Extract data
        results = destinations()
        destinations_data = json.loads(results.data)
        destinations_option = destinations_data["option"]
        
        # Case: no option given or wrong option
        if destinations_option == "redirect":
            return make_response(
                redirect("/home", code=302)
            )
        
        # Case: good option
        return make_response(
            render_template("destinations.html", option = destinations_option)
        )
        
    return make_response(
        redirect("/login", code=302)
    )