import mysql.connector
import requests
import time
from PIL import Image


# Unsplash keys
acces_key = "3uY2o4LBYoeowPX3Fhv7E8T-1m3OLpa04DLwJ7eV5Ms"
secret_key = "Vi4KCDIN62dTQf4-fPKRBX0dGE0bUpUOZRWJUyMH6vU"


# Capitals of Europe
capitals = ["Amsterdam",
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

# TODO -> delete current photos before downloading the new ones

# Connect to dba
dba = mysql.connector.connect(host='localhost', password='mysqlradu', user='radu', database='travel_with_us')
# Create cursor
dba_cursor = dba.cursor()

# For every destination, extract a image link and insert it into the database
for capital in capitals:

    # Extract content using Unsplash API
    api_url = f"https://api.unsplash.com/search/photos?page=1&per_page=1&order_by=relevant&orientation=landscape&query={capital}&client_id=3uY2o4LBYoeowPX3Fhv7E8T-1m3OLpa04DLwJ7eV5Ms"
    response = requests.get(api_url)

    print("Status code: ", response.status_code)

    # Transform data in json format
    json_data = response.json()

    # Extract only the url from the json formatted data
    image_url = json_data["results"][0]["urls"]["raw"]

    # Insert url into dba
    dba_cursor.execute("UPDATE `destinations` SET `image_link`=%s WHERE `name`=%s", (image_url, capital,))

    # Write images
    try:
        with open("webapp/static/assets/photos/" + capital + ".jpg", "wb") as file:
            response_two = requests.get(image_url, stream=True)
            file.write(response_two.content)
    except:
        print("Folder not found.")

    # Wait to prevent crashes
    time.sleep(1)


# Close cursor and commit the changes
dba_cursor.close()
dba.commit()


# For every destination, extract its correspondent image and set new dimensions (size decreasing)
for capital in capitals:
    # Open the image file
    image = Image.open("webapp/static/assets/photos/" + capital + ".jpg")

    # Set the new size
    new_size = (400, 267)

    # Resize the image
    resized_image = image.resize(new_size)

    # Save the resized image
    resized_image.save("webapp/static/assets/photos/" + capital + ".jpg")