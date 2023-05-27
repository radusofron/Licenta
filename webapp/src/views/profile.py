from controllers.profile import profile
from flask import Blueprint, make_response, render_template, session, redirect
from flask.wrappers import Response
from flask_api import status
import json


profile_view_blueprint = Blueprint("profile_view_blueprint", __name__)


@profile_view_blueprint.route("/profile")
def profile_view() -> Response:
    # User is not logged in
    if not session["logged_in"]:
        return make_response(
            redirect("/login", code=302)
        )
    
    # Extract data
    results = profile()
    profile_data = json.loads(results.data)
    user_profile_data = profile_data["user profile data"]
    visited_percentage = profile_data["visited percentage"]
    visited_destinations_last_years = profile_data["visited destinations last years"]
    years = profile_data["years"]
    visited_destinations_per_year = profile_data["visited destinations per year"]
  
    return make_response(
        render_template("profile.html", user_profile_data = user_profile_data, visited_percentage = visited_percentage, 
                        visited_destinations_last_years = visited_destinations_last_years, years = years, 
                        visited_destinations_per_year = visited_destinations_per_year)
    )