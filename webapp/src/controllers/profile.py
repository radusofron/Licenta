from flask import Blueprint, make_response, jsonify, session, request, redirect
from flask_api import status
from flask.wrappers import Response
from database import dba, extract_username_by_id, extract_email_by_id, extract_registration_date_by_id, extract_visited_destinations_number, extract_destinations_number, extract_visited_destinations_number_by_date
import datetime


profile_controller_blueprint = Blueprint("profile_controller_blueprint", __name__)


def process_destinations_number(destinations_number: str) -> str:
    """Function adds a 0 in front of 1 digit strings
    """
    if len(destinations_number) == 1:
        destinations_number = "0" + destinations_number
    return destinations_number


def compute_year_n_years_ago(years_ago: int) -> int:
    """Function returns the year from n years ago
    """
    # Get the current year
    current_year = datetime.datetime.now().year
    # Compute desired year
    start_year = current_year - years_ago
    return start_year


@profile_controller_blueprint.route("/api/profile", methods=['GET', 'POST'])
def profile() -> Response:
    # POST request:
    if request.method == "POST":
        print("This was a post request")
        return make_response(
            redirect("/profile", code=302)
        )
    
    # GET request:
    # Extract user account details
    username = extract_username_by_id(dba, session["user_id"])
    email = extract_email_by_id(dba, session["user_id"])
    date = extract_registration_date_by_id(dba, session["user_id"])

    # Convert date to string format
    date = date.strftime('%Y-%m-%d %H:%M:%S') # type: ignore
    
    # Create a list with them
    user_profile_data = [username, email, date]

    # Extract user's visited destinations number and total number
    visited_destinations = extract_visited_destinations_number(dba, session["user_id"])
    all_destinations = extract_destinations_number(dba)
    # Compute stat with them
    visited_percentage = round(int(visited_destinations) * 100 / int(all_destinations), 1) # type: ignore
    visited_percentage = str(visited_percentage) + "%"

    # Extract starting year for the stats
    starting_year = compute_year_n_years_ago(4)

    # Extract user's visited destinations number starting from the previously extracted year and process it
    visited_destinations_last_years = extract_visited_destinations_number_by_date(dba, starting_year, session["user_id"], 1)
    visited_destinations_last_years = process_destinations_number(str(visited_destinations_last_years))

    # Compute the years from the previously extracted year untill now and
    # extract the user's visited destinations numbers for the extracted year and for each computed year
    years = []
    visited_destinations_per_year = []
    for unit in range(5):
        year = starting_year + unit
        years.append(year)
        visited_destinations_per_year.append(extract_visited_destinations_number_by_date(dba, year, session["user_id"], 2))
    print("This is standard")
        
    return make_response(
        jsonify({"user profile data": user_profile_data, "visited percentage": visited_percentage, "visited destinations last years": visited_destinations_last_years, "years": years, "visited destinations per year": visited_destinations_per_year}),
        status.HTTP_200_OK,
    )

