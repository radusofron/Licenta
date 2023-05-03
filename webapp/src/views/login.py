from flask import Blueprint, make_response, render_template, session
from flask.wrappers import Response
from flask_api import status
import json

login_view_blueprint = Blueprint("login_view_blueprint", __name__)


@login_view_blueprint.route("/login")
def login_view() -> Response:
    return make_response(
        render_template("login.html")
    )