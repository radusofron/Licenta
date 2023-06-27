from flask import Blueprint, make_response, jsonify, session
from flask_api import status
from flask.wrappers import Response
from database import dba, extract_destinations_average_grade, extract_destinations_good_overall_feeling_reviews, extract_destinations_total_reviews


statistics_controller_blueprint = Blueprint("statistics_controller_blueprint", __name__)


def get_raitings_data():
    """Function extracts and processes the raitings of the cities
    """
    destinations_average_grade = extract_destinations_average_grade(dba)

    # Transform from Decimal to float and round
    float_destinations_average_grade = []
    for destination_average_grade in destinations_average_grade:
        avg_grade = str(destination_average_grade[0])
        float_avg_grade = round(float(avg_grade), 2)
        float_destination_average_grade = (float_avg_grade, destination_average_grade[1])
        float_destinations_average_grade.append(float_destination_average_grade)
    
    return float_destinations_average_grade


def get_reviews_data():
    """Function extracts reviews' general feeling and computes how many good general feelings every city has
    """
    good_reviews = extract_destinations_good_overall_feeling_reviews(dba) 
    reviews = extract_destinations_total_reviews(dba)

    # Compute good reviews percentages
    percentages = []
    for good_review in good_reviews:
        for review in reviews:
            if good_review[1] == review[1]:
                new_percentage = (round(int(good_review[0]) * 100 / int(review[0]), 2), good_review[1]) # type: ignore
                percentages.append(new_percentage)

    return percentages


@statistics_controller_blueprint.route("/api/statistics")
def statistics() -> Response:

    # 1. Get raitings data for graph
    average_grades = get_raitings_data()

    # 2. Get reviews data for graph
    percentages = get_reviews_data()

    return make_response(
        jsonify({"average grades": average_grades, "percentages": percentages}),
        status.HTTP_200_OK,
    )