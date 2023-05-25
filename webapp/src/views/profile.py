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
  
    return make_response(
        render_template("profile.html")
    )