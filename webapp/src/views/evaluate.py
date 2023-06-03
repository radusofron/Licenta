from controllers.evaluate import evaluate
from flask import Blueprint, make_response, render_template, session, redirect
from flask.wrappers import Response
from flask_api import status
import json


evaluate_view_blueprint = Blueprint("evaluate_view_blueprint", __name__)


@evaluate_view_blueprint.route("/evaluate")
def evaluate_view() -> Response:
    # User is not logged in
    if not session["logged_in"]:
        return make_response(
            redirect("/login", code=302)
        )
    
    # Extract data
    results = evaluate()
    destination_data = json.loads(results.data)
    option = destination_data["option"]
    
    # Case: no option given or wrong option
    if option == "redirect":
        return make_response(
            redirect("/destinations?option=visited", code=302)
        )

    # Case: good option
    

    return make_response(
        render_template("evaluate.html")
    )