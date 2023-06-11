from controllers.index import index
from flask import Blueprint, make_response, render_template, session
from flask.wrappers import Response
from flask_api import status
import json


index_view_blueprint = Blueprint("index_view_blueprint", __name__)


@index_view_blueprint.route("/")
def index_view() -> Response:

    # Session exited
    session["logged_in"] = False

    # Extract data
    results = index()
    index_data = json.loads(results.data)
    most_visited = index_data["most visited"]
    reviews = index_data["reviews"]

    return make_response(
        render_template("index.html", most_visited = most_visited, reviews = reviews)
    )