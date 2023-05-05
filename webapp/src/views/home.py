from controllers.index import index
from flask import Blueprint, make_response, render_template, session, redirect, url_for
from flask.wrappers import Response
from flask_api import status
import json

home_view_blueprint = Blueprint("home_view_blueprint", __name__)


@home_view_blueprint.route("/home")
def home_view() -> Response:
    if session["logged_in"]:
        return make_response(
            render_template("home.html")
        )
    return make_response(
        redirect("/login", code=302)
    )