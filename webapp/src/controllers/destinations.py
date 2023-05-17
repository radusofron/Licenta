from flask import Blueprint, make_response, jsonify, session, request
from flask_api import status
from flask.wrappers import Response
from database import dba, extract_user_visited_destinations, extract_user_wishlisted_destinations


destinations_controller_blueprint = Blueprint("destinations_controller_blueprint", __name__)


@destinations_controller_blueprint.route("/api/destinations")
def destinations() -> Response:
    # Extract option
    option = request.args.get("option")

    # List to store specific destinations (based on option chosen)
    specific_destinations = []

    # Case: no option given or wrong option
    if option is None or option not in ["visited", "wishlisted", "all"]:
        option = "redirect"
    
    # Case: visited
    elif option == "visited":
        visited_destinations = extract_user_visited_destinations(dba, session["user_id"])
        # Case: visited destinations found
        if len(visited_destinations):
            for tpl in visited_destinations:
                specific_destinations.append(tpl[0])
    
    # Case: wishlisted
    elif option == "wishlisted":
        wishlisted_destinations = extract_user_wishlisted_destinations(dba, session["user_id"])
        # Case: wishlisted destinations found
        if len(wishlisted_destinations):
            for tpl in wishlisted_destinations:
                specific_destinations.append(tpl[0])

    # Case: all
    else:
        specific_destinations = ["Most visited"]

    # Common
    destinations = ["All"]
    
    return make_response(
        jsonify({"option": option, "specific destinations": specific_destinations, "all destinations": destinations}),
        status.HTTP_200_OK,
    )