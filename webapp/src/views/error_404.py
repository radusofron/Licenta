from flask import Blueprint, make_response, session, redirect
from flask.wrappers import Response


error_404_view_blueprint = Blueprint("error_404_view_blueprint", __name__)


@error_404_view_blueprint.app_errorhandler(404)
def page_not_found(error_404) -> Response:

    # If user is logged in, redirect to home, else, redirect to login
    if session["logged_in"]:
        return make_response(
            redirect("/home", code=302)
        )
    else:
        return make_response(
            redirect("/login", code=302)   
        )