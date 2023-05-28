from flask import Blueprint, make_response, jsonify, session, request, redirect, flash
from flask_api import status
from flask.wrappers import Response
from database import dba, extract_username_by_id, extract_email_by_id, extract_registration_date_by_id, login_validation, update_password, delete_account_and_associated_data, extract_visited_destinations_number, extract_destinations_number, extract_visited_destinations_number_by_date
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
        # Identify form
        # 1. Upload photo
        if "upload" in request.form:
            photo = request.files['photo']
            print(photo)
            # TODO -> validate file size using javascript before enable upload photo button
        # 2. Change password
        elif "change" in request.form:
            # Extract change password input data
            current_password = request.form["password"]
            new_password = request.form["new-password"]
            new_password_confirmation = request.form["new-password-confirmation"]

            # Check if the new password meets the requirements
            if len(new_password) < 8:
                flash("password_error")
            elif new_password != new_password_confirmation:
                flash("passwords_error")
            else:
                # Extract user email
                email = extract_email_by_id(dba, session["user_id"])
                
                # Return password validation
                answear = login_validation(dba, str(email), current_password)

                # If password was validated, proceed accordingly
                if answear:
                    update_password(dba, new_password, session["user_id"])
                    flash("success")
                else:
                    flash("current_password")
        # 3. Delete account
        elif "delete" in request.form:
            delete_account_and_associated_data(dba, session["user_id"])
            # Redirect user to landing page
            return make_response(
                redirect("/", code=302)
            )

        # Redirect user to the same page
        return make_response(
            redirect("/profile", code=302)
        )
    
    # GET request:
    # Extract user account details
    username = extract_username_by_id(dba, session["user_id"])
    email = extract_email_by_id(dba, session["user_id"])
    date = extract_registration_date_by_id(dba, session["user_id"])

    # Convert date to string format
    date = date.strftime('%d.%m.%Y  %H:%M:%S') # type: ignore
    
    # Create a list with them
    user_profile_data = [username, email, date]

    # Extract user's visited destinations number and total number
    visited_destinations = extract_visited_destinations_number(dba, session["user_id"])
    all_destinations = extract_destinations_number(dba)
    # Compute stat with them
    visited_percentage = round(int(visited_destinations) * 100 / int(all_destinations), 2) # type: ignore
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

    # Store data for visited destinations graph in a dictionary
    visited_destinations_graph_data = dict()
    visited_destinations_graph_data["last_years"] = visited_destinations_last_years
    visited_destinations_graph_data["years"] = years
    visited_destinations_graph_data["per_year"] = visited_destinations_per_year
        
    return make_response(
        jsonify({"user profile data": user_profile_data, "visited percentage": visited_percentage, "visited destinations graph data": visited_destinations_graph_data}),
        status.HTTP_200_OK,
    )

