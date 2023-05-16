from controllers.home import home
from flask import Blueprint, make_response, render_template, session, redirect
from flask.wrappers import Response
from flask_api import status
import json


home_view_blueprint = Blueprint("home_view_blueprint", __name__)


@home_view_blueprint.route("/home")
def home_view() -> Response:
    if session["logged_in"]:
        results = home()
        home_data = json.loads(results.data)
        total_destinations = home_data["total destinations"]
        wishlisted_destinations = home_data["wishlisted destinations"]
        visited_destinations = home_data["visited destinations"]
        return make_response(
            render_template("home.html", total_destinations = total_destinations, wishlisted_destinations = wishlisted_destinations, visited_destinations = visited_destinations)
        )
    return make_response(
        redirect("/login", code=302)
    )