import mysql.connector
import requests


# Unsplash keys
acces_key = "3uY2o4LBYoeowPX3Fhv7E8T-1m3OLpa04DLwJ7eV5Ms"
secret_key = "Vi4KCDIN62dTQf4-fPKRBX0dGE0bUpUOZRWJUyMH6vU"


# Capitals of europe
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
    "Minsk",
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


# Connect to dba
dba = mysql.connector.connect(host='localhost', password='mysqlradu', user='radu', database='travel_with_us')
# Create cursor
dba_cursor = dba.cursor()

# For every destination, extract a image link and insert it into the database
for capital in capitals:

    # Extract content using Unsplash API
    api_url = f"https://api.unsplash.com/search/photos?page=1&per_page=1&order_by=relevant&orientation=landscape&query={capital}&client_id=3uY2o4LBYoeowPX3Fhv7E8T-1m3OLpa04DLwJ7eV5Ms"
    response = requests.get(api_url)

    # Transform data in json format
    json_data = response.json()

    # Extract only the url from the json formatted data
    image_url = json_data["results"][0]["urls"]["raw"]

    # Insert url into dba
    dba_cursor.execute("UPDATE `destinations` SET `image_link`=%s WHERE `name`=%s", (image_url, capital,))

# Close cursor and commit the changes
dba_cursor.close()
dba.commit()