from flask import Blueprint, make_response, jsonify, session, request, redirect, flash, current_app, url_for
from flask_api import status
from flask.wrappers import Response
from werkzeug.utils import secure_filename
from database import dba, update_profile_picture_relative_path, extract_photo_name, extract_username_by_id, extract_email_by_id, extract_registration_date_by_id, login_validation, update_password, delete_account_and_associated_data, extract_visited_destinations_number, extract_destinations_number, extract_visited_destinations_number_by_date
import datetime
from PIL import Image
import os


profile_controller_blueprint = Blueprint("profile_controller_blueprint", __name__)


# POST functions
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
def get_visited_percentage() -> str:
    """Function calculates the percentage of destinations visited by the user out of the total available 
    destinations.
    """
    # Extract user's visited destinations number and total number
    visited_destinations = extract_visited_destinations_number(dba, session["user_id"])
    all_destinations = extract_destinations_number(dba)
    
    # Compute stat with them
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


def process_destinations_number(destinations_number: str) -> str:
    """Function adds a 0 in front of 1 digit strings
    """
    if len(destinations_number) == 1:
        destinations_number = "0" + destinations_number
    return destinations_number


def get_visited_graph_data() -> dict:
    """
    """
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

    return visited_destinations_graph_data


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
            # Remove account profile picture
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
    date = date.strftime('%d.%m.%Y  %H:%M:%S') # type: ignore

    # Create a list with them
    user_profile_data = [profile_picture, username, email, date]

    # Visited destinations section
    # 1. Get visited percentage
    visited_percentage = get_visited_percentage()
    # 2. Get graph data
    visited_graph_data = get_visited_graph_data()

    # Evaluation section
        
    return make_response(
        jsonify({"user profile data": user_profile_data, "has profile picture": has_profile_picture ,"visited percentage": visited_percentage, "visited graph data": visited_graph_data}),
        status.HTTP_200_OK,
    )

