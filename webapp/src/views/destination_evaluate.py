from controllers.destination_evaluate import destination_evaluate
from flask import Blueprint, make_response, render_template, session, redirect
from flask.wrappers import Response
from flask_api import status
import json


destination_evaluate_view_blueprint = Blueprint("destination_evaluate_view_blueprint", __name__)


@destination_evaluate_view_blueprint.route("/evaluate")
def destination_evaluate_view() -> Response:
    # User is not logged in
    if not session["logged_in"]:
        return make_response(
            redirect("/login", code=302)
        )
    
    # Extract data
    results = destination_evaluate()
    evaluation_data = json.loads(results.data)
    option = evaluation_data["option"]
    
    # Case: no option given or wrong option
    if option == "redirect":
        return make_response(
            redirect("/destinations?option=visited", code=302)
        )

    # Case: good option
    visited_date = evaluation_data["visited date"]
    aspects = evaluation_data["aspects"]
    user_feedback = evaluation_data["user feedback"]

    return make_response(
        render_template("destination_evaluate.html", option = option, visited_date = visited_date, aspects = aspects, user_feedback = user_feedback)
    )