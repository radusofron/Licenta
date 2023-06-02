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
    has_profile_picture = profile_data["has profile picture"]
    visited_percentage = profile_data["visited percentage"]
    visited_destinations_graph_data = profile_data["visited graph data"]
  
    return make_response(
        render_template("profile.html", user_profile_data = user_profile_data, has_profile_picture = has_profile_picture, visited_percentage = visited_percentage, 
                        visited_destinations_graph_data = visited_destinations_graph_data)
    )