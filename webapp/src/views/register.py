from flask import Blueprint, make_response, render_template, session
from flask.wrappers import Response
from flask_api import status
import json

register_view_blueprint = Blueprint("register_view_blueprint", __name__)


@register_view_blueprint.route("/register")
def register_view() -> Response:
    return make_response(
        render_template("register.html")
    )