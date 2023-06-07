import mysql.connector
import requests
import urllib.parse


cities = [
    "Amsterdam",
    "Athens",
    "Belgrade",
    "Berlin",
    "Bern",
    "Bratislava",
    "Bucharest",
    "Brussels",
    "Budapest",
    "Chisinau",
    "Copenhagen",
    "Dublin",
    "Helsinki",
    "Kiev",
    "Lisbon",
    "Ljubljana",
    "London",
    "Madrid",
    "Moscow",
    "Oslo",
    "Paris",
    "Prague",
    "Reykjavik",
    "Riga",
    "Rome",
    "Sarajevo",
    "Skopje",
    "Sofia",
    "Stockholm",
    "Tallinn",
    "Tirana",
    "Vienna",
    "Vilnius",
    "Warsaw",
    "Zagreb"]


def connect_to_dba():
    """Function connects to database.
    """
    # Database connection details
    dba_host = 'localhost'
    dba_user = 'radu'
    dba_password = 'mysqlradu'
    dba_name = 'travel_with_us'
    
    # Connect to database
    dba = mysql.connector.connect(host=dba_host, password=dba_password, user=dba_user, database=dba_name)
    return dba


def extract_destination_id_by_name(dba, destination_name: str) -> int:
    """Function returns the id of a destination based on its name.
    """
    # Extract average grades
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `id` FROM destinations WHERE `name`=%s", (destination_name,))
    destination_id = dba_cursor.fetchone()
    dba_cursor.close()
    
    # Case: no id returned
    if destination_id is None:
        return 0
    return destination_id[0]


def get_city_coordinates(city: str) -> tuple:
    """Function retrieves the coordinates (latitude and longitude) of a given city.
    
    Function is called in get_city_touristic_objectives.
    """
    # Read OpenCage Geocoding API key
    try:
        with open("webapp/static/API_keys/OpenCage.txt", "r") as file:
            key = file.read()
    except:
        return ()

    # URI Encoding for city name
    city = urllib.parse.quote(city)

    # Create url
    url = f"https://api.opencagedata.com/geocode/v1/json?q={city}&key={key}&limit=1&pretty=1"
    # Create request
    response = requests.get(url)
    # Get json format
    response = response.json()

    # Get coordinates
    latitude = response["results"][0]["geometry"]["lat"]
    longitude = response["results"][0]["geometry"]["lng"]

    # TODO -> insert city coordinates in destinations table

    return (longitude, latitude)


def get_city_touristic_objectives(dba, city: str):
    """Function retrives 500 touristic objectives for a given city, then inserts them into the database.
    """
    try:
        with open("webapp/static/API_keys/Geoapify.txt", "r") as file:
            key = file.read()
    except:
        return ()

    # Data for API
    category = "tourism"
    meters = 5000
    limit = 500

    # Extract coordinates of the city
    coordinates = get_city_coordinates(city)

    # Create url
    url = f"https://api.geoapify.com/v2/places?categories={category}&filter=circle:{coordinates[0]},{coordinates[1]},{meters}&limit={limit}&lang=en&apiKey={key}"
    # Create request
    response = requests.get(url)
    # Get json format
    response = response.json()

    # Start to process data
    touristic_objectives = dict()
    index = 0

    # Open cursor
    dba_cursor = dba.cursor()

    # Extract city ID
    destination_id = extract_destination_id_by_name(dba, city)

    # Process every touristic objective found
    for touristic_objective in response["features"]:
        # New dictionary, one for every touristic objective
        new_data = {"name": "", "coordinates": {"longitude": 0, "latitude": 0}, "id": ""}

        # Add data
        if "name" in touristic_objective["properties"]:
            new_data["name"] = touristic_objective["properties"]["name"]
            # Skip if not found
            if "formatted" in touristic_objective["properties"]:
                new_data["address"] = touristic_objective["properties"]["formatted"]
            else:
                new_data["address"] = None
            # Skip if not found
            if "opening_hours" in touristic_objective["properties"]["datasource"]["raw"]:
                new_data["opening_hours"] = touristic_objective["properties"]["datasource"]["raw"]["opening_hours"]
            else:
                new_data["opening_hours"] = None
            new_data["coordinates"]["longitude"] = float(touristic_objective["geometry"]["coordinates"][0])
            new_data["coordinates"]["latitude"] = float(touristic_objective["geometry"]["coordinates"][1])
            new_data["place_id"] = touristic_objective["properties"]["place_id"]

            # Write in database
            dba_cursor.execute("INSERT INTO `touristic_objectives` (`destination_id`, `name`, `address`, `longitude`, `latitude`, `opening_hours`, `place_id`) VALUES (%s, %s, %s, %s, %s, %s, %s)", (destination_id, new_data["name"], new_data["address"], new_data["coordinates"]["longitude"], new_data["coordinates"]["latitude"], new_data["opening_hours"], new_data["place_id"]))

    
    # Close cursor and commit changes
    dba_cursor.close()
    dba.commit()


def delete_previous_touristic_objectives(dba):
    """Function deletes the previously added touristic objectives from the database.
    """
    # Open cursor
    dba_cursor = dba.cursor()

    # Delete from database
    dba_cursor.execute("DELETE FROM `touristic_objectives`")

    # Close cursor and commit changes
    dba_cursor.close()
    dba.commit()


def main():
    # Connect to database (creating database object)
    dba = connect_to_dba()

    # Delete all the data from database
    delete_previous_touristic_objectives(dba)

    # Extract toursitic objectives for every city
    for city in cities:
        print("For city: ", city)
        get_city_touristic_objectives(dba, city)

    # Close connection to database
    dba.close()


main()