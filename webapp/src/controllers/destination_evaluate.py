from flask import Blueprint, make_response, jsonify, session, request, redirect, flash, get_flashed_messages
from flask_api import status
from flask.wrappers import Response
from database import dba, extract_destinations_names, extract_visited_destination_date_for_user, insert_visited_destination_evaluation_by_user, extract_visited_destination_evaluation_by_user, update_visited_destination_evaluation_by_user, insert_visited_destination_review_by_user, extract_visited_destination_review_by_user, update_visited_destination_review_by_user


destination_evaluate_controller_blueprint = Blueprint("destination_controller_blueprint", __name__)


def create_list_from_list_with_tuples(list_with_tuples: list[tuple]) -> list:
    """Function creates a list containing all the data

    Database's function returns a list with tuples containing the data

    This function returns a list containing the data
    """
    new_list = []

    # Parse the list with the tuples and add data in a new list
    if len(list_with_tuples):
        for tpl in list_with_tuples:
            new_list.append(tpl[0])

    return new_list


def validate_url_parameters():
    """Function validates url parameters. All possible cases included
    """
    # Extract city
    city = request.args.get("city")

    # Extract available destinations 
    destinations = extract_destinations_names(dba)
    destinations = create_list_from_list_with_tuples(destinations)

    # Case: no city given
    if city is None:
        action = "redirect"
        return action
    
    # Transform city to start with capital letter then lowercase letters
    city = str(city).capitalize()

    # Case: wrong city
    if city not in destinations:
        action = "redirect"
        return action
    
    # City exists
    action = city

    return action


def get_evaluation_aspects() -> list[str]:
    """Function returns evaluation aspects
    """
    aspects = ["Attractions", "Accomodation", "Culture", "Entertainment", "Food and drink", 
              "History", "Natural beauty", "Night life", "Transport", "Safety"]
    return aspects


def get_general_feelings() -> list[str]:
    """Function returns general feelings
    """
    general_feelings = ["delighted", "satisfied", "neutral", "disappointed", "frustrated"]
    return general_feelings


def extract_input_grades() -> list[int]:
    """Function extracts the grades given by an user as input
    """
    # Extract aspects in order to extract the grades
    aspects = get_evaluation_aspects()

    # Extract grades
    grades = []
    for aspect in aspects:
        grades.append(int(request.form[aspect]))
    
    return grades


def get_visited_date(city: str):
    """Function extracts and processes the date when the city was marked as visited by the user
    """
    visited_date = extract_visited_destination_date_for_user(dba, session["user_id"], city)
    visited_date = visited_date.strftime('%d %b %Y')  # type: ignore
    return visited_date


@destination_evaluate_controller_blueprint.route("/api/evaluate", methods=['GET', 'POST'])
def destination_evaluate() -> Response:
    # POST request:
    if request.method == "POST":

        # Identify form
        # 1. Send evaluation
        if "evaluate" in request.form:
            # Extract grades
            grades = extract_input_grades()

            # Insert evaluation
            insert_visited_destination_evaluation_by_user(dba, session["user_id"], session["current_city"], grades)
            flash("evaluation submitted")

        # 2. Update evaluation
        elif "update-evaluation" in request.form:
            # Extract grades
            grades = extract_input_grades()

            # Update evaluation
            update_visited_destination_evaluation_by_user(dba, session["user_id"], session["current_city"], grades)
            flash("evaluation updated")

        # 3. Send review
        elif "leave-review" in request.form:
            # Extract general feeling
            general_feeling = request.form["feeling"]

            # Extract review
            review = request.form["review"]

            # Insert review
            insert_visited_destination_review_by_user(dba, session["user_id"], session["current_city"], review, general_feeling)
            flash("review submitted") 

        elif "update-review" in request.form:
            # Extract general feeling
            general_feeling = request.form["feeling"]

            # Extract review
            review = request.form["review"]

            # Update review
            update_visited_destination_review_by_user(dba, session["user_id"], session["current_city"], review, general_feeling)
            flash("review updated") 
            
        return make_response(
            redirect("/evaluate?city=" + session["current_city"], code=302)
        )

    # GET request:

    # Check validation status
    option = validate_url_parameters()

    # Case: redirect
    if option == "redirect":
        return make_response(
            jsonify({"option": option}),
            status.HTTP_200_OK,
        )

    # Case: city exists

    # Save city in session
    session["current_city"] = option

    # 1. Get visited destination date
    visited_date = get_visited_date(option)
    
    # 2. Get evaluation grades and review
    user_feedback = dict()
    user_feedback["evaluation"] = extract_visited_destination_evaluation_by_user(dba, session["user_id"], option)
    user_feedback["review"] = extract_visited_destination_review_by_user(dba, session["user_id"], option)

    # 3. Get evaluation content
    aspects = get_evaluation_aspects()

    # 4. Get general feelings
    general_feelings = get_general_feelings()
        
    return make_response(
        jsonify({"option": option, "visited date": visited_date, "aspects": aspects, "general feelings": general_feelings, "user feedback": user_feedback}),
        status.HTTP_200_OK,
    )