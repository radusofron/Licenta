from flask import Blueprint, make_response, jsonify
from flask_api import status
from flask.wrappers import Response
from database import dba, extract_the_three_most_visited_destinations, extract_three_most_recent_website_reviews

index_controller_blueprint = Blueprint("index_controller_blueprint", __name__)


@index_controller_blueprint.route("/api")
def index() -> Response:
    # Extract most visited destinations
    most_visited = extract_the_three_most_visited_destinations(dba)

    # Extract three website reviews
    reviews = extract_three_most_recent_website_reviews(dba)

    # Process the list (case: there are not 3 visited destinations yet)
    while len(most_visited) < 3:
        most_visited.append(tuple(["no data available"]))

    # Process the list (case: there are not 3 reviews shorter than 100 characters yet)
    while len(reviews) < 3:
        reviews.append(tuple(["no data available", "no data available"]))

    return make_response(
        jsonify({"most visited": most_visited, "reviews": reviews}),
        status.HTTP_200_OK,
    )