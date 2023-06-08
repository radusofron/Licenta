import mysql.connector
import requests
import time
from PIL import Image
import os


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
    """Function creates a folder named "covers" where there will be a cover photo for every city.
    
    If the folder already exists, function skips.
    """

    # Create folder path
    folder_path = "webapp/static/assets/cities_photos/covers"

    # Check if folder exists, otherwise, create it
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)


def extract_city_cover_photo(cities):
    """Function extracts a cover photo for every city.
    """
    # Read Unsplash API key
    try:
        with open("webapp/static/API_keys/Unsplash.txt", "r") as file:
            key = file.read()
    except:
        return None
    
    # Connect to dba
    dba = mysql.connector.connect(host='localhost', password='mysqlradu', user='radu', database='travel_with_us')
    # Create cursor
    dba_cursor = dba.cursor()

    # For every city, get a cover photo and insert its path into database
    for city in cities:

        # Create url
        url = f"https://api.unsplash.com/search/photos?page=1&per_page=1&order_by=relevant&orientation=landscape&query={city}&client_id={key}"
        # Create request
        response = requests.get(url)

        # Get json format
        json_data = response.json()

        # Extract image url
        image_url = json_data["results"][0]["urls"]["raw"]

        # Write image
        try:
            with open("webapp/static/assets/cities_photos/covers/" + city + ".jpg", "wb") as file:
                # Create request
                response_two = requests.get(image_url, stream=True)
                file.write(response_two.content)
        except:
            return None

        # Wait to prevent crashes
        time.sleep(2)

    # Close cursor and commit the changes
    dba_cursor.close()
    dba.commit()

    # Close connection to database
    dba.close()


def resize_images(cities: list[str]):
    """Function resizes all the covor photos. (Dimension decreasing)
    """
    # For every city, extract its correspondent photo and set new dimensions (size decreasing)
    for city in cities:
        # Open the image file
        image = Image.open("webapp/static/assets/cities_photos/covers" + city + ".jpg")

        # Set the new size
        new_size = (400, 267)

        # Resize the image
        resized_image = image.resize(new_size)

        # Save the resized image
        resized_image.save("webapp/static/assets/cities_photos/covers" + city + ".jpg")


def main():
    extract_city_cover_photo(cities)
    resize_images(cities)


main()