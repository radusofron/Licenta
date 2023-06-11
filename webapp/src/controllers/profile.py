from flask import Blueprint, make_response, jsonify, session, request, redirect, flash, current_app, url_for
from flask_api import status
from flask.wrappers import Response
from werkzeug.utils import secure_filename
from database import dba, update_profile_picture_relative_path, extract_photo_name, extract_username_by_id, extract_email_by_id, extract_registration_date_by_id, login_validation, update_password, delete_account_and_associated_data, extract_visited_destinations_number, extract_destinations_number, extract_visited_destinations_number_by_date, extract_evaluated_destinations_number, extract_evaluated_destinations_total_grade, extract_destination_name_by_id
import datetime
from PIL import Image
import os


profile_controller_blueprint = Blueprint("profile_controller_blueprint", __name__)


# POST functions
def remove_itineraries_representation():
    """Function removes all the representations of the itineraries created by the user
    """
    # Designated folder path
    folder_path = "webapp/static/user_data/" + str(session["user_id"])
    
    # List files of the folder
    files = os.listdir(folder_path)

    # Remove every file of the folder
    for file in files:
        os.remove(folder_path + "/" + file)

    # Remove empty folder
    os.rmdir(folder_path)


def remove_profile_picture():
    """Function removes user's previous profile picture if it exists or the last profile picture when an account is deleted.
    """
    # Designated folder for profile picture
    folder_path = current_app.config["UPLOAD_FOLDER"]

    # List files of the folder
    files = os.listdir(folder_path)

    # Iterate through files of the folder
    for file in files:
        filename = file[:file.find(".")]
        if filename == str(session["user_id"]):
            os.remove(folder_path + "/" + file)


def resize_profile_picture(photo_relative_path: str):
    """Function resizes the given image if it is big
    """
    # Resize file
    image = Image.open(photo_relative_path)

    # Get file dimensions
    width, height = image.size

    # Compute dimension coefficient
    if width >= height:
        coefficient = width / height
    else:
        coefficient = height / width


    # Set the new size
    if width >= height and height > 750:
        new_size = (int(750 * coefficient), 750)
    elif height > width and width > 750:
        new_size = (750, int(750 * coefficient))
    else:
        return

    # Resize the image
    resized_photo = image.resize(new_size)

    # Save the resized image
    resized_photo.save(photo_relative_path)


def upload_profile_picture():
    """Function extracts profile picture file and proceeds accordingly
    """
    # Get photo
    photo = request.files["photo"]

    # Check photo name to exists
    if not photo.filename:
        return None
    # First, remove user's previous photo stored
    remove_profile_picture()   

    # Then, extract photo name in order to extract photo extension
    photo_name = secure_filename(photo.filename)
    photo_extension = photo_name[(photo_name.rfind(".") + 1):]
    
    # Compute photo path and photo new name
    photo_new_name = str(session["user_id"]) + "." + photo_extension
    photo_relative_path = current_app.config["UPLOAD_FOLDER"] +  photo_new_name
    
    # Save file
    photo.save(photo_relative_path)
    
    # Resize photo to reduce its size if it's possible
    resize_profile_picture(photo_relative_path)

    # Insert photo path
    update_profile_picture_relative_path(dba, photo_new_name, session["user_id"])


def change_password():
    """Function changes user's password if validations are successfully made
    """
    # Extract change password input data
    current_password = request.form["password"]
    new_password = request.form["new-password"]
    new_password_confirmation = request.form["new-password-confirmation"]

    # Check if new password meets the requirements
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


# GET functions
def get_visited_percentage(visited_destinations: int) -> str:
    """Function calculates the percentage of destinations visited by the user out of the total available 
    destinations.
    """
    # Extract total number of destinations
    all_destinations = extract_destinations_number(dba)
    
    # Compute percentage
    visited_percentage = round(visited_destinations * 100 / all_destinations, 2)
    visited_percentage = str(visited_percentage) + "%"

    return visited_percentage


def compute_year_n_years_ago(years_ago: int) -> int:
    """Function returns the year from n years ago
    """
    # Get the current year
    current_year = datetime.datetime.now().year
    # Compute desired year
    start_year = current_year - years_ago
    return start_year


def get_visited_graph_data() -> dict:
    """
    """
    # Extract starting year for the stats
    starting_year = compute_year_n_years_ago(4)

    # Extract user's visited destinations number starting from the previously extracted year and process it
    visited_destinations_last_years = extract_visited_destinations_number_by_date(dba, starting_year, session["user_id"], 1)
    visited_destinations_last_years = str(visited_destinations_last_years).zfill(2)

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

    return visited_destinations_graph_data


def get_evaluation_percentage(visited_destinations: int) -> str:
    """Function calculates the percentage of destinations evaluated by the user out of the total visited
    destinations.
    """
    # Extract user's evaluated destinations number
    evaluated_destinations = extract_evaluated_destinations_number(dba, session["user_id"])

    # Compute percentage
    evaluated_percentage = round(evaluated_destinations * 100 / max(visited_destinations, 1), 2)
    evaluated_percentage = str(evaluated_percentage) + "%"

    return evaluated_percentage


def get_evaluation_data() -> dict:
    # Get destinations grades sum
    evaluated_destinations_grades_sum = extract_evaluated_destinations_total_grade(dba, session["user_id"])

    # Case: no destinations evaluated
    if not len(evaluated_destinations_grades_sum):
        return dict()
    
    # Case: maximum a desitnation evaluated
    if len(evaluated_destinations_grades_sum) <= 1:
        return dict()

    # Evaluation fields
    total = 10

    # Calculate favourite destination and average grade
    favourite_destination = [0, 0]
    average_grade = 0
    for destination in evaluated_destinations_grades_sum:
        average_grade += destination[1]
        if destination[1] > favourite_destination[1]:
            favourite_destination[1] = destination[1]
            favourite_destination[0] = destination[0]
    average_grade = round(average_grade / (total * len(evaluated_destinations_grades_sum)), 2)
        
    # Calculate least favourite destination
    least_favourite_destination = [0, 0]
    for destination in evaluated_destinations_grades_sum:
        if destination[1] < favourite_destination[1]:
            least_favourite_destination[1] = destination[1]
            least_favourite_destination[0] = destination[0]

    # Extract names for favourite destination and least favourite destination
    favourite_destination_name = extract_destination_name_by_id(dba, favourite_destination[0])
    least_favourite_destination_name = extract_destination_name_by_id(dba, least_favourite_destination[0])

    # Calculate average grades for favourite destination and least favourite destination
    favourite_destination_grade = round(favourite_destination[1] / total)
    least_favourite_destination_grade = round(least_favourite_destination[1] / total, 2)
    
    # Create dictionary with them
    evaluation_stats = dict()
    evaluation_stats["most"] = [favourite_destination_name, favourite_destination_grade]
    evaluation_stats["least"] = [least_favourite_destination_name, least_favourite_destination_grade]
    evaluation_stats["average"] = average_grade

    return evaluation_stats


@profile_controller_blueprint.route("/api/profile", methods=['GET', 'POST'])
def profile() -> Response:
    # POST request:
    if request.method == "POST":

        # Identify form
        # 1. Upload photo
        if "upload" in request.form:
            upload_profile_picture()

        # 2. Change password
        elif "change" in request.form:
            change_password()

        # 3. Delete account
        elif "delete" in request.form:

            # Delete itineraries' representation
            remove_itineraries_representation()

            # Delete account profile picture
            remove_profile_picture()

            # Delete account from database
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
    photo_name = extract_photo_name(dba, session["user_id"])
    username = extract_username_by_id(dba, session["user_id"])
    email = extract_email_by_id(dba, session["user_id"])
    date = extract_registration_date_by_id(dba, session["user_id"])

    # If photo name not found, upload default profile picture
    if photo_name is None:
        # Default profile picture
        profile_picture = str(username)[:2].upper()
        has_profile_picture = False
    else:
        # Existent profile picture
        profile_picture = str(photo_name)
        has_profile_picture = True

    # Convert date to string format
    date = date.strftime('%d %b %Y at %H:%M:%S') # type: ignore

    # Create a list with them
    user_profile_data = [profile_picture, username, email, date]

    # Get user's visited destinations number
    visited_destinations_number = extract_visited_destinations_number(dba, session["user_id"])

    # Visited destinations section
    # 1. Get visited percentage
    visited_percentage = get_visited_percentage(visited_destinations_number)
    # 2. Get graph data
    visited_graph_data = get_visited_graph_data()

    # Evaluation section
    # 1. Get evaluation percentage
    evaluated_percentage = get_evaluation_percentage(visited_destinations_number)
    # 2. Get favourite destination, least favourite destination, their average grades and general average grade
    evaluation_data = get_evaluation_data()
        
    return make_response(
        jsonify({"user profile data": user_profile_data, "has profile picture": has_profile_picture ,"visited percentage": visited_percentage, "visited graph data": visited_graph_data, "evaluated percentage": evaluated_percentage, "evaluation data": evaluation_data}),
        status.HTTP_200_OK,
    )

