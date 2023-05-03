from flask import Blueprint, make_response, jsonify, redirect, request
from flask_api import status
from flask.wrappers import Response

register_controller_blueprint = Blueprint("register_controller_blueprint", __name__)


@register_controller_blueprint.route("/api/register", methods = ["POST"])
def register():
    return redirect("/home", code=302)
