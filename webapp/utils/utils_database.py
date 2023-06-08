import mysql.connector


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


def update_destination_coordinates(dba, destination_name: str, longitude: float, latitude: float):
    """Function updates the coordinates of a destination into the database.
    """
    # Open cursor
    dba_cursor = dba.cursor()

    # Insert coordinates
    dba_cursor.execute("UPDATE `destinations` SET `longitude`=%s, `latitude`=%s WHERE `name`=%s", (longitude, latitude, destination_name))

    # Close cursor and commit changes
    dba_cursor.close()
    dba.commit()


def extract_destination_coordinates(dba, destination_name: str):
    """Function returns the coordinates of a destination from database.
    """
    # Extract desitnation coordinates
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `longitude`, `latitude` FROM destinations WHERE `name`=%s", (destination_name,))
    coordinates = dba_cursor.fetchone()
    dba_cursor.close()

    return coordinates


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


def insert_touristic_objective(dba, destination_name: str, touristic_objective: dict):
    """Function inserts touristic objective of a destination into the database.
    """
    # Extract destination id
    destination_id = extract_destination_id_by_name(dba, destination_name)

    # Open cursor
    dba_cursor = dba.cursor()

    # Insert touristic objective
    dba_cursor.execute("INSERT INTO `touristic_objectives` (`destination_id`, `name`, `address`, `longitude`, `latitude`, `opening_hours`, `place_id`) VALUES (%s, %s, %s, %s, %s, %s, %s)", (destination_id, touristic_objective["name"], touristic_objective["address"], touristic_objective["coordinates"]["longitude"], touristic_objective["coordinates"]["latitude"], touristic_objective["opening_hours"], touristic_objective["place_id"]))

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


def close_connection_to_dba(dba):
    """Function closes the connection with the database.
    """
    dba.close()


# Connect to database (creating database object)
dba = connect_to_dba()