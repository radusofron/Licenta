from flask import Blueprint, make_response, jsonify, session, request, redirect, flash, get_flashed_messages
from flask_api import status
from flask.wrappers import Response
from database import dba, extract_destinations_names, extract_destination_id_by_name, extract_destination_average_grades, extract_destination_reviews, insert_wishlisted_destination_for_user, delete_wishlisted_destination_for_user, insert_visited_destination_for_user, delete_visited_destination_for_user, update_traveler_level_for_user, extract_touristic_objectives_names, extract_touristic_objective_coordinates_by_name, insert_itinerary_for_user
import requests
from datetime import datetime, timedelta
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from sklearn.cluster import KMeans
import uuid
import urllib.parse
from collections import Counter


destination_details_controller_blueprint = Blueprint("destination_details_controller_blueprint", __name__)


def create_list_with_destinations(destinations: list) -> list:
    """Function creates a list containing all the destinations names

    Database's function returns a list with tuples containing the names 

    This function returns a list containing the names
    """
    list_with_destiantions = []

    # Parse the list with the tuples and add the names in a new list
    if len(destinations):
        for tpl in destinations:
            list_with_destiantions.append(tpl[0])

    return list_with_destiantions


def validate_url_parameters():
    """Function validates url parameters. All possible cases included
    """
    # Extract city
    city = request.args.get("city")

    # Extract available destinations 
    destinations = extract_destinations_names(dba)
    destinations = create_list_with_destinations(destinations)

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


def create_city_folder(city: str):
    """Function creates a folder for every city (if the city already has a folder, then it skips that city).
    """

    # Create folder path
    folder_path = "webapp/static/destinations_data/" + city

    # Check if folder exists, otherwise, create it
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)


def check_for_POST_messages():
    """Function check for messages recieved from a previous POST request.

    If there are messages, function proceeds accordingly to them modifying session data.
    """
    messages = get_flashed_messages()
    if messages:
        # Proceed as the action says
        if messages[0] == "add to wishlist":
            session["wishlisted_destinations"].insert(0, messages[1])
        elif messages[0] == "remove from wishlist":
            session["wishlisted_destinations"].remove(messages[1])
        elif messages[0] == "mark as visited":
            session["visited_destinations"].insert(0, messages[1])
        elif messages[0] == "remove from visited":
            session["visited_destinations"].remove(messages[1])


def check_visited_status(city: str) -> bool:
    """Function determines whether the city has been marked as visited by the user or not
    """
    if city in session["visited_destinations"]:
        return True
    return False


def check_wishlisted_status(city: str) -> bool:
    """Function determines whether the city has beenadded to wishlist by the user or not
    """
    if city in session["wishlisted_destinations"]:
        return True
    return False


def get_wiki_content(city: str):
    """Function extracts Wikipedia information for a given city
    """
    # Create request
    response = requests.get("https://en.wikipedia.org/w/api.php?action=query&prop=extracts&titles=" + city + "&format=json")

    # Exit if request was not successfull
    if response.status_code != 200:
        return "";

    # Jsonify content
    json_content = response.json()

    # Parse the json in order to extract the content
    content = ""
    for id in json_content["query"]["pages"]:
        content = json_content["query"]["pages"][id]["extract"]
 
    return content


def get_statistics_grades(city: str) -> dict:
    """Function extracts statistics for a given city
    """
    statistics = {"names": [], "grades": []}
    statistics["names"] = ["Attractions", "Accomodation", "Culture", "Entertainment", "Food and drink", 
              "History", "Natural beauty", "Night life", "Transport", "Safety"]
    statistics["grades"] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # Extract destination id
    destination_id = extract_destination_id_by_name(dba, city)
    
    # Case: wrong city
    if not destination_id:
        return statistics
    
    # City exists
    # Extract desitnation grades
    grades = extract_destination_average_grades(dba, destination_id)
    
    # Case: destination has no grades
    if not len(grades):
        return statistics
    
    # Create a list with floats
    float_grades = []

    # Grades exist
    # Convert Decimal to str then to float
    for index in range(10):
        float_grades.append(str(grades[0][index]))
        float_grades[index] = float(float_grades[index])
        float_grades[index] = round(float_grades[index], 1)

    # Update dictionary
    statistics["grades"] = float_grades

    return statistics


def change_date_format(date) -> str:
    """Function recieves a date and returns the time passed from that date untill now
    """
    current_date = datetime.now()

    # Different years
    if date.year < current_date.year:
        return str(current_date.year - date.year) + " year(s) ago"
    
    # Different months
    if date.month < current_date.month:
        return str(current_date.month - date.month) + " month(s) ago"
    
    # Different days
    if date.day < current_date.day:
        return str(current_date.day - date.day) + " day(s) ago"

    # Different hours
    if date.hour < current_date.hour:
        return str(current_date.hour - date.hour) + " hour(s) ago"
    
    # Different minutes
    if date.minute < current_date.minute:
        return str(current_date.minute - date.minute) + " minute(s) ago"
    
    return "Now"


def get_traveler_degree(traveler_level: str):
    """Function returns traveler degree.
    
    Traveler degree  makes filtering easier.
    """
    if traveler_level == "master":
        return 0
    elif traveler_level == "expert":
        return 1
    elif traveler_level == "advanced":
        return 2
    elif traveler_level == "intermediate":
        return 3
    elif traveler_level == "beginner":
        return 4
    elif traveler_level == "novice":
        return 5
    

def get_feeling_degree(general_feeling: str):
    """Function returns feeling degree.

    Feeling degree makes filtering easier.
    """
    if general_feeling == "delighted":
        return 0
    elif general_feeling == "impressed":
        return 1
    elif general_feeling == "satisfied":
        return 2
    elif general_feeling == "neutral":
        return 3
    elif general_feeling == "disappointed":
        return 4
    elif general_feeling == "bored":
        return 5
    elif general_feeling == "frustrated":
        return 6
        

def get_reviews_and_associated_data(city: str) -> dict:
    """Function extracts reviews for a given city
    """
    # Extract destination id
    destination_id = extract_destination_id_by_name(dba, city)

    # Case: wrong city
    if not destination_id:
        return dict()
    
    # City exists
    # Extract desitnation grades
    reviews_rows = extract_destination_reviews(dba, destination_id)

    # Case: destination has no reviews
    if not len(reviews_rows):
        return dict()
    
    # Create dictionary
    reviews = {"username": [], "photo_name": [], "date": [], "traveler_level": [], "feeling": [], "review": [], "traveler_degree": [], "feeling_degree": []}
    for row in reviews_rows:
        reviews["username"].append(str(row[0]))
        reviews["photo_name"].append(row[1])
        reviews["date"].append(row[2])
        reviews["traveler_level"].append(str(row[3]).lower())
        reviews["feeling"].append(str(row[4]))
        reviews["review"].append(str(row[5]))
        # Add traveler level degree and feeling degree
        reviews["traveler_degree"].append(get_traveler_degree(str(reviews["traveler_level"][-1])))
        reviews["feeling_degree"].append(get_feeling_degree(str(reviews["feeling"][-1])))

    # If user has no photo change photo_name to 0, otherwise transform to string
    for index in range(len(reviews["photo_name"])):
        if reviews["photo_name"][index] is None:
            reviews["photo_name"][index] = "0"
        else:
            reviews["photo_name"][index] = str(reviews["photo_name"][index])

    # Change date format
    for index in range(len(reviews["date"])):
        reviews["date"][index] = change_date_format(reviews["date"][index])
    
    return reviews


def update_news(city: str):
    """Function retrieves and updates the news for a given city every 12 hours to avoid excesive API calls.
    
    Function writes news details in a correspondent JSON file.
    """
    # Read Weather Map API key
    try:
        with open("webapp/static/API_keys/GNews.txt", "r") as file:
            key = file.read()
    except:
        return None
    
    # Create json name and json path
    json_name = "news" + ".json"
    json_path = "webapp/static/destinations_data/" + city + "/" + json_name

    if os.path.exists(json_path):
        # Case: check last update
        last_modification_timestamp = os.path.getmtime(json_path)
        # Convert from timestamp to datetime
        last_modification_time = datetime.fromtimestamp(last_modification_timestamp)

        # Calcualte time elapsed since the last modification
        current_date = datetime.now()
        # Return time elapsed in seconds
        time_elapsed = (current_date - last_modification_time).total_seconds()
        # Convert to hours
        hours_elapsed = time_elapsed /  3600

        # Check if 12 hours have elapsed since the last modification
        if hours_elapsed < 12:
            # Case: no update
            return None
        
    # Case: update
    # Create url
    url = f"https://gnews.io/api/v4/search?q={city}&lang=en&max=10&apikey={key}"
    # Create request
    response = requests.get(url)
    # Get json format
    response = response.json()

    # Write news data in correspondent json file
    try:
        with open(json_path, "w") as file:
            json.dump(response, file)
    except:
        return None


def read_news(city: str):
    """Function reads the news from a correspondent JSON file and processes the required 
    information for website
    """
    # Create json name and json path
    json_name = "news" + ".json"
    json_path = "webapp/static/destinations_data/" + city + "/" + json_name

    # Extract news
    try:
        with open(json_path, "r") as file:
            news = json.load(file)
    except:
        return []
    
    news_list = []
    # Create a list for every news and append it to main list
    for a_news in news["articles"]:
        news_element = [a_news["title"], a_news["description"], a_news["image"], a_news["url"], a_news["source"]["name"], a_news["source"]["url"]]
        news_list.append(news_element)

    return news_list


def update_weather(city: str):
    """Function retrieves and updates the weather details of a given city at most once per hour to avoid excesive API calls.

    Function writes weather details in a correspondent JSON file.
    """
    # Read Weather Map API key
    try:
        with open("webapp/static/API_keys/OpenWeatherMap.txt", "r") as file:
            key = file.read()
    except:
        return None

    # Create json name and json path
    json_name = "weather" + ".json"
    json_path = "webapp/static/destinations_data/" + city + "/" + json_name

    if os.path.exists(json_path):
        # Case: check last update
        last_modification_timestamp = os.path.getmtime(json_path)
        # Convert from timestamp to datetime
        last_modification_time = datetime.fromtimestamp(last_modification_timestamp)

        # Calcualte time elapsed since the last modification
        current_date = datetime.now()
        # Return time elapsed in seconds
        time_elapsed = (current_date - last_modification_time).total_seconds()
        # Convert to hours
        hours_elapsed = time_elapsed /  3600

        # Check if an hour has elapsed since the last modification
        if hours_elapsed < 1:
            # Case: no update
            return None
        
    # Case: update
    # Create url
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={key}&units=metric"
    # Create request
    response = requests.get(url)
    # Get json format
    response = response.json()

    # Write weather data in correspondent json file
    try:
        with open(json_path, "w") as file:
            json.dump(response, file)
    except:
        return None
    

def read_weather(city: str) -> list:
    """Function reads weather details from a correspondent JSON file and processes the required 
    information for website
    """
    # Create json name and json path
    json_name = "weather" + ".json"
    json_path = "webapp/static/destinations_data/" + city + "/" + json_name

    # Extract wether details
    try:
        with open(json_path, "r") as file:
            weather_details = json.load(file)
    except:
        return []
    
    # Create a list for every day
    day_1 = []
    day_2 = []
    day_3 = []
    day_4 = []

    # Extract current date
    current_date = datetime.now()

    for index in range(40):

        # Convert timestamp to datetime
        weather_date = datetime.fromtimestamp(weather_details["list"][index]["dt"])

        # Create a dictionary for every day, modify hour format and convert temperatures to int
        if weather_date.day == current_date.day:
            day_1.append((str(weather_date.hour) + ":00").zfill(5))
            day_1.append(weather_details["list"][index]["weather"][0]["main"])
            day_1.append(round(weather_details["list"][index]["main"]["temp"]))
            day_1.append(round(weather_details["list"][index]["main"]["feels_like"]))
        elif len(day_2) < 32:
            day_2.append((str(weather_date.hour) + ":00").zfill(5))
            day_2.append(weather_details["list"][index]["weather"][0]["main"])
            day_2.append(round(weather_details["list"][index]["main"]["temp"]))
            day_2.append(round(weather_details["list"][index]["main"]["feels_like"]))
        elif len(day_3) < 32:
            day_3.append((str(weather_date.hour) + ":00").zfill(5))
            day_3.append(weather_details["list"][index]["weather"][0]["main"])
            day_3.append(round(weather_details["list"][index]["main"]["temp"]))
            day_3.append(round(weather_details["list"][index]["main"]["feels_like"]))
        elif len(day_4) < 32:
            day_4.append((str(weather_date.hour) + ":00").zfill(5))
            day_4.append(weather_details["list"][index]["weather"][0]["main"])
            day_4.append(round(weather_details["list"][index]["main"]["temp"]))
            day_4.append(round(weather_details["list"][index]["main"]["feels_like"]))
    
    # Create a list containing all the lists
    days = [day_1, day_2, day_3, day_4]

    return days


def get_weather_days() -> list:
    """Function returns the days for which the weather is available
    """
    # Already know the first 2 days
    days = ["Today", "Tomorrow"]

    # Extract current date
    current_date = datetime.now()

    # Calculate the last 2 days and modify their format
    date_3 = current_date + timedelta(days = 2)
    day_3 = str(date_3.day).zfill(2) + "." + str(date_3.month).zfill(2)
    date_4 = current_date + timedelta(days = 3)
    day_4 = str(date_4.day).zfill(2) + "." + str(date_4.month).zfill(2)
    
    # Add them to list
    days.append(day_3)
    days.append(day_4)

    return days


def colors_for_clusters(clusters):
    """Function sets different colors for clusters representation
    """
    colors = []
    for point in clusters:
        if point == 0:
            colors.append("#608DB8")
        elif point == 1:
            colors.append("#BB493A")
        elif point == 2:
            colors.append("#FFA90A")
        elif point == 3:
            colors.append("#3D9537")
        elif point == 4:
            colors.append("#3B3941")
        elif point == 5:
            colors.append("#F397D6")
        elif point == 6:
            colors.append("#8338EC")
            
    return colors


def create_user_folder(folder_name: str):
    """Function creates a folder for an user containing his travel itineraries representations.

    If user already has a folder, then nothing happens.
    """

    # Create folder path
    folder_path = "webapp/static/user_data/" + folder_name

    # Check if folder exists, otherwise, create it
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)


def create_travel_itinerary(days: int, objectives: list[str], algorithm: str, itinerary: dict):
    """Function creates travel itinerary based on user's options
    """
    # Extract touristic objectives details
    objectives_details = []
    for objective in objectives:
        objectives_details.extend(extract_touristic_objective_coordinates_by_name(dba, objective))
    
    # Create pandas dataframe
    df = pd.DataFrame(objectives_details, columns=["Name", "Longitude", "Latitude"])
    # Convert from string to float
    df["Longitude"] = df["Longitude"].astype(float)
    df["Latitude"] = df["Latitude"].astype(float)

    # FOR BOTH algorithms
    # -------------------
    # Group touristic objectives using kmeans (using Euclidean distance)
    km = KMeans(n_clusters=days, init='k-means++')
    global clusters
    clusters = km.fit_predict(df[["Longitude", "Latitude"]])

    # Convert to list
    clusters = clusters.tolist()

    # ONLY FOR MODIFIED algorithm
    # ---------------------------
    if algorithm == "modified":

        # Determine desired cardinal of clusters
        desired_cardinal = len(objectives) // days
        remaining = len(objectives) - desired_cardinal * days

        # Compute cardinal of every cluster
        clusters_cardinals = Counter(clusters)

        # Determine which clusters must remove elements and which clusters must add elements
        overloaded_clusters = []
        underloaded_clusters = []
        for cluster_index in range(days):
            if clusters_cardinals[cluster_index] < desired_cardinal:
                underloaded_clusters.append(cluster_index)
            elif clusters_cardinals[cluster_index] > desired_cardinal:
                overloaded_clusters.append(cluster_index)

        # Proceed only if underloaded clusters exists, otherwise don't modify
        if len(underloaded_clusters) > 0:

            # Extract centroids coordinates
            centroids = km.cluster_centers_
            # Convert to list
            centroids = centroids.tolist()

            # Create dicitonary to store the attractions for every cluster
            cluster = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
            # Create list to store the attractions used
            used_attractions = []
            # For every cluster
            for current_cluster in clusters_cardinals.keys():
                # Create dictionary key
                cluster[current_cluster] = []
                # For every tourist objective
                for attraction_index in range(len(objectives)):
                    # Compute the Manhattan distance between every attraction and the current cluster
                    lat_dist = abs(df.loc[attraction_index, "Latitude"] - centroids[current_cluster][0])
                    long_dist = abs(df.loc[attraction_index, "Longitude"] - centroids[current_cluster][1])
                    total_distance = lat_dist + long_dist
                    # Add attraction index and its distance to specific dictionary
                    cluster[current_cluster].append([attraction_index, total_distance])
                # Remove attractions that were already used
                cluster_copy = cluster[current_cluster].copy() 
                for element in cluster_copy:
                    if element[0] in used_attractions:
                        cluster[current_cluster].remove(element)
                # Add the desired number of attractions for cluster
                if remaining > 0:
                    cluster[current_cluster] = sorted(cluster[current_cluster], key=lambda x: x[1])[:(desired_cardinal + 1)]
                    remaining -= 1
                else:
                    cluster[current_cluster] = sorted(cluster[current_cluster], key=lambda x: x[1])[:desired_cardinal]
                # Store used attractions
                for element in cluster[current_cluster]:
                    used_attractions.append(element[0])
                # Store positions
                cluster_copy = cluster[current_cluster].copy()
                cluster[current_cluster] = []
                for element in cluster_copy:
                    cluster[current_cluster].append(element[0])

            clusters = []
            # Add clusters lists to same list
            for attraction in sorted(used_attractions):
                if attraction in cluster[0]:
                    clusters.append(0)
                elif attraction in cluster[1]:
                    clusters.append(1)
                elif attraction in cluster[2]:
                    clusters.append(2)
                elif attraction in cluster[3]:
                    clusters.append(3)
                elif attraction in cluster[4]:
                    clusters.append(4)
                elif attraction in cluster[5]:
                    clusters.append(5)
                elif attraction in cluster[6]:
                    clusters.append(6)

    # Group objectives by clusters
    # Create a string containing all the objectives of a group, for every group
    objectives_groups = {"day1": "", "day2": "", "day3": "", "day4": "", "day5": "", "day6": "", "day7": ""}
    # The objectives of a group are delimitated using 
    delimiter = "####"
    for index in range(len(objectives)):
        if clusters[index] == 0:
            objectives_groups["day1"] = objectives_groups["day1"] + objectives[index] + delimiter
        elif clusters[index] == 1:
            objectives_groups["day2"] = objectives_groups["day2"] + objectives[index] + delimiter
        elif clusters[index] == 2:
            objectives_groups["day3"] = objectives_groups["day3"] + objectives[index] + delimiter
        elif clusters[index] == 3:
            objectives_groups["day4"] = objectives_groups["day4"] + objectives[index] + delimiter
        elif clusters[index] == 4:
            objectives_groups["day5"] = objectives_groups["day5"] + objectives[index] + delimiter
        elif clusters[index] == 5:
            objectives_groups["day6"] = objectives_groups["day6"] + objectives[index] + delimiter
        elif clusters[index] == 6:
            objectives_groups["day7"] = objectives_groups["day7"] + objectives[index] + delimiter

    # Set colors for clusters
    colors = colors_for_clusters(clusters)

    # Create cluster representation
    # 1. Set backend for writing to file
    matplotlib.use("agg")
    # Set colors and create figure
    plt.figure(facecolor = "#F2F2F2")
    axes = plt.axes()
    axes.scatter(df["Longitude"], df["Latitude"], color = colors, alpha=0.5)
    axes.set_facecolor("#F2F2F2")

    # Save representation
    create_user_folder(str(session["user_id"]))
    # Create itinerary id
    itinerary["id"] = urllib.parse.quote(str(uuid.uuid4()))
    plt.savefig("webapp/static/user_data/" + str(session["user_id"]) + "/" + itinerary["id"] +  ".png")

    # Insert itinerary into the database
    insert_itinerary_for_user(dba, itinerary, session["user_id"], session["current_city"], 
                                objectives_groups)

    # Return itinerary id
    return itinerary["id"]


# POST function:
def calculate_traveler_level(option: int):
    """Function calculates new traveler level for user

    Parameters:
        * option = 1 -> new visited destination, so adds one to the length
        * option = 0 -> visited destination remove, so one less from the length 
    """
    # Calculate visited destinations number
    if option:
        number = len(session["visited_destinations"]) + 1
    else:
        number = len(session["visited_destinations"]) - 1

    # Determine traveler level
    if number <= 2:
        traveler_level = "Novice"
    elif number > 2 and number <= 5:
        traveler_level = "Beginner"
    elif number > 5 and number <= 10:
        traveler_level = "Intermediate"
    elif number > 10 and number <= 20:
        traveler_level = "Advanced"
    elif number > 20 and number <= 30:
        traveler_level = "Expert"
    else:
        traveler_level = "Master"
    
    return traveler_level


@destination_details_controller_blueprint.route("/api/destination_details", methods=['GET', 'POST'])
def destination_details() -> Response:
    # POST request:
    if request.method == "POST":

        # Identify form
        # 1. Add to wishlist
        if "add-wishlist" in request.form:
            insert_wishlisted_destination_for_user(dba, session["user_id"], session["current_city"])
            flash("add to wishlist")

        # 2. Remove from wishlist
        elif "remove-wishlist" in request.form:
            delete_wishlisted_destination_for_user(dba, session["user_id"], session["current_city"])
            flash("remove from wishlist")

        # 3. Mark as visited & calculate new traveler level
        elif "mark-visited" in request.form:

            # Mark as visited
            insert_visited_destination_for_user(dba, session["user_id"], session["current_city"])

            # Update traveler level
            traveler_level = calculate_traveler_level(1)
            update_traveler_level_for_user(dba, session["user_id"], traveler_level)

            # Send message
            flash("mark as visited")

        # 4. Remove from visited
        elif "remove-visited" in request.form:

            # Remove from visited
            delete_visited_destination_for_user(dba, session["user_id"], session["current_city"])

            # Update traveler level
            traveler_level = calculate_traveler_level(0)
            update_traveler_level_for_user(dba, session["user_id"], traveler_level)

            # Send message
            flash("remove from visited")

        # 5. Generate travel itinerary
        elif "generate" in request.form:
            # Extract form data
            days = int(request.form["days"])
            objectives = request.form.getlist("objective")
            algorithm = request.form["algorithm"]
            # Create dictionary to store itinerary details
            itinerary = dict()
            itinerary["name"] = request.form.get("name", "")
            itinerary["description"] = request.form.get("description", "")

            # Create itinerary
            itinerary_id = create_travel_itinerary(days, objectives, algorithm, itinerary)

            return make_response(
                redirect("/itineraries?id=" + itinerary_id, code=302)
            )

        # Send city and action via flash
        flash(session["current_city"])

        return make_response(
            redirect("/destination?city=" + session["current_city"], code=302)
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

    # Create city folder if not found
    create_city_folder(option)

    # Check for possible messages recieved from a previous POST request
    check_for_POST_messages()

    # Save city in session
    session["current_city"] = option

    # 0. Get city status for user
    city_status = dict()
    city_status["visited"] = check_visited_status(option)
    city_status["wishlisted"] = check_wishlisted_status(option)

    # 1. Get touristic objectives
    touristic_objectives = extract_touristic_objectives_names(dba, option)

    # 2. Get Wikipedia content
    wikipedia = get_wiki_content(option)

    # 3. Create websites for photos links
    websites_links = []
    websites_links.append("https://www.pexels.com/search/" + option + "/")
    websites_links.append("https://unsplash.com/s/photos/" + option)

    # 4. Get statistics
    statistics = get_statistics_grades(option)

    # 5. Get reviews
    reviews = get_reviews_and_associated_data(option)
    
    # 6. Update news, get news
    update_news(option)
    news_data = read_news(option)
    
    # 7. Update weather, get weather details, calculate weather days and create dictionary with data
    update_weather(option)
    weather = read_weather(option)
    days = get_weather_days()
    weather_data = {"names": days, "weather": weather}
    # Case: weather not available for today anymore
    if not len(weather_data["weather"][0]):
        weather_data["names"].remove("Today")
        del weather_data["weather"][0]
        
    return make_response(
        jsonify({"option": option, "city status": city_status , "touristic objectives": touristic_objectives, "wikipedia": wikipedia, "websites links": websites_links, "statistics": statistics, "reviews": reviews, "news data": news_data, "weather data": weather_data}),
        status.HTTP_200_OK,
    )