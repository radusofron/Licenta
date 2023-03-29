from controllers.index import index
from flask import Blueprint, make_response, render_template, session
from flask.wrappers import Response
from flask_api import status
import json

login_view_blueprint = Blueprint("login_view_blueprint", __name__)


@login_view_blueprint.route("/login")
def login_view() -> Response:
    result = index()
    if result.status_code == status.HTTP_404_NOT_FOUND:
        return make_response(render_template("login.html"))

    json_data = json.loads(result.data)
    data = json_data["data"]
    text = json_data["text"]
    number = json_data["number"]
    a = json_data["a"]
    session["data"] = data  # salvare de date in sesiune generala

    return make_response(
        render_template("login.html", data=data, text=text, number=number, a=a)
    )