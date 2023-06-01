import mysql.connector
import requests
import time
from PIL import Image
import os


# Unsplash keys
acces_key = "3uY2o4LBYoeowPX3Fhv7E8T-1m3OLpa04DLwJ7eV5Ms"
secret_key = "Vi4KCDIN62dTQf4-fPKRBX0dGE0bUpUOZRWJUyMH6vU"


# Capitals of Europe
cities = [
    "Amsterdam",
    "Athens",
    "Belgrade",
    "Berlin",
    "Bern",
    "Bratislava",
    "Brussels",
    "Bucharest",
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


def prepare_folder(city: str):
    """Function creates a folder for every city (if the city already has a folder, then it skips that city).
    
    Also, removes all the files found in a city folder.
    """

    # Create folder path
    folder_path = "webapp/static/assets/cities_photos/" + city

    # Check if folder exists, otherwise, create it
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    # Remove existing files
    files = os.listdir(folder_path)
    for file in files:
        os.remove(folder_path + "/" + file)


def extract_city_photos(cities: list[str]):
    """Function extracts 20 photos for every city.
    """
    for city in cities:

        # Prepare city folder
        prepare_folder(city)

        # Extract content using Unsplash API
        api_url = f"https://api.unsplash.com/search/photos?page=1&per_page=20&order_by=relevant&orientation=landscape&query={city}&client_id=3uY2o4LBYoeowPX3Fhv7E8T-1m3OLpa04DLwJ7eV5Ms"
        response = requests.get(api_url)

        # Exit if request was not successfull
        if response.status_code != 200:
            print("A iesit ca nu mai am request-uri disponibile.")
            return None

        # Jsonify content
        json_data = response.json()

        # For every photo, extract only the url from the json formatted data and write the image
        for index in range(20):
            image_url = json_data["results"][index]["urls"]["raw"]

            # Write image
            try:
                with open("webapp/static/assets/cities_photos/" + city + "/" + str(index) + ".jpg", "wb") as file:
                    # Extract image
                    response_two = requests.get(image_url, stream=True)
                    file.write(response_two.content)
            except:
                print("Something went wrong...")

        # Wait to prevent crashes
        time.sleep(1)


def resize_images(cities: list[str]):
    """Function resizes all the 20 photos for every city. (Dimension decreasing)
    """
    for city in cities:
        print("City: ", city)
        for index in range(20):
            print("\tImage: ", index)
            # Open the image file
            image = Image.open("webapp/static/assets/cities_photos/" + city + "/" + str(index) + ".jpg")

            # Set the new size
            new_size = (800, 534)

            # Resize the image
            resized_image = image.resize(new_size)

            # Save the resized image
            resized_image.save("webapp/static/assets/cities_photos/" + city + "/" + str(index) + ".jpg")


# extract_city_photos(cities)
resize_images(cities)

