import requests
import urllib.parse
from utils_database import dba, update_destination_coordinates, close_connection_to_dba


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


def get_destination_coordinates(city: str):
    """Function retrieves the coordinates (latitude and longitude) of a given city, then inserts them into
    the database.
    """
    # Read OpenCage Geocoding API key
    try:
        with open("webapp/static/API_keys/OpenCage.txt", "r") as file:
            key = file.read()
    except:
        print("Exception!")
        return

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

    # Update coordinates into the database
    update_destination_coordinates(dba, city, longitude, latitude)


def main():
    # Extract coordinates for every city
    for city in cities:
        get_destination_coordinates(city)

    # Close database connection
    close_connection_to_dba(dba)


main()