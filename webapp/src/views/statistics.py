from controllers.statistics import statistics
from flask import Blueprint, make_response, render_template, session, redirect
from flask.wrappers import Response
from flask_api import status
import json


statistics_view_blueprint = Blueprint("statistics_view_blueprint", __name__)


@statistics_view_blueprint.route("/statistics")
def statistics_view() -> Response:
    # User is not logged in
    if not session["logged_in"]:
        return make_response(
            redirect("/login", code=302)
        )
    
    # Extract data
    results = statistics()
    statistics_data = json.loads(results.data)
    average_grades = statistics_data["average grades"]
    return make_response(
        render_template("statistics.html", average_grades = average_grades)
    )    