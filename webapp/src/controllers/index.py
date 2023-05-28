from flask import Blueprint, make_response, jsonify
from flask_api import status
from flask.wrappers import Response
from database import dba, extract_most_visited_destinations

index_controller_blueprint = Blueprint("index_controller_blueprint", __name__)


@index_controller_blueprint.route("/api")
def index() -> Response:
    # Extract most visited destinations
    most_visited = extract_most_visited_destinations(dba)

    # TODO -> extract 3 websites reviews

    # Process the list (case: there are not 3 visited destinations yet)
    while len(most_visited) < 3:
        most_visited.append(tuple(["no data available"]))

    return make_response(
        jsonify({"most visited": most_visited}),
        status.HTTP_200_OK,
    )