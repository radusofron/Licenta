import requests
from utils_database import dba, extract_destination_coordinates, delete_previous_touristic_objectives, insert_touristic_objective, close_connection_to_dba


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
    coordinates = extract_destination_coordinates(dba, city)

    # Create url
    url = f"https://api.geoapify.com/v2/places?categories={category}&filter=circle:{coordinates[0]},{coordinates[1]},{meters}&limit={limit}&lang=en&apiKey={key}"
    # Create request
    response = requests.get(url)
    # Get json format
    response = response.json()

    # Start to process data
    touristic_objectives = dict()
    index = 0

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
            
            # Insert touristic objective into the database
            insert_touristic_objective(dba, city, new_data)


def main():
    # Delete all the touristic objectives from database
    delete_previous_touristic_objectives(dba)

    # Extract toursitic objectives for every city
    for city in cities:
        print("For city: ", city)
        get_city_touristic_objectives(dba, city)

    # Close database connection
    close_connection_to_dba(dba)


main()