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

    return make_response(
        render_template("index.html")
    )