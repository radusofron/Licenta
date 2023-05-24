import mysql.connector
import time
from werkzeug.security import generate_password_hash, check_password_hash


def connect_to_dba():
    """Function connects to database
    """
    # Database connection details
    dba_host = 'localhost'
    dba_user = 'radu'
    dba_password = 'mysqlradu'
    dba_name = 'travel_with_us'
    
    # Connect to database
    dba = mysql.connector.connect(host=dba_host, password=dba_password, user=dba_user, database=dba_name)
    return dba


def extract_most_visited_destinations(dba):
    """Function returns most visited destinations on our website
    """
    # Extract them
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `d`.`name` FROM `destinations` `d` INNER JOIN `visited_destinations` `v` ON `d`.`id`=`v`.`destination_id` GROUP BY `destination_id` ORDER BY COUNT(*) DESC LIMIT 3")
    most_visited = dba_cursor.fetchall()
    dba_cursor.close()
    return most_visited


def login_validation(dba, input_email: str, input_password: str) -> bool:
    """Function returns login status
    """
    # Extract user credentials
    email = extract_user_email(dba, input_email)
    if len(email) == 1:
        password = extract_user_password(dba, input_email)
        if check_password_hash(password[0][0], input_password):
            return True
    return False


def extract_user_id(dba, input_email):
    """Function returns user id from database based on email given
    """
    # Extract id
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `id` FROM `users` WHERE `email`=%s", (input_email,))
    user_id = dba_cursor.fetchone()
    dba_cursor.close()
    return user_id[0]


def extract_user_username(dba, input_username: str):
    """Function returns user username from database
    """
    # Extract username
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `username` FROM `users` WHERE `username`=%s", (input_username,))
    username = dba_cursor.fetchall()
    dba_cursor.close()
    return username


def extract_user_email(dba, input_email: str):
    """Function returns user email from database
    """
    # Extract email
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `email` FROM `users` WHERE `email`=%s", (input_email,))
    email = dba_cursor.fetchall()
    dba_cursor.close()
    return email


def extract_user_password(dba, input_email: str):
    """Function returns user password from database based on email given
    """
    # Extract password
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `password` FROM `users` WHERE `email`=%s", (input_email,))
    password = dba_cursor.fetchall()
    dba_cursor.close()
    return password


def extract_user_max_id(dba):
    """Function returns the biggest user id from database
    """
    # Extract maximum id number
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT MAX(`id`) FROM `users`")
    max_id = dba_cursor.fetchone()
    dba_cursor.close()
    return max_id[0]


def insert_user(dba, username: str, email: str, password: str):
    """Function inserts user to database
    """
    # Extract biggest user id found
    max_id = extract_user_max_id(dba)

    # Compute new user id
    if max_id is None:
        # Case: first insertion
        new_max_id = 1
    else:
        # Case: the other insertions
        new_max_id = max_id + 1

    # Hash the password
    encrypted_password = generate_password_hash(password)

    # Extract date
    date_time = time.strftime('%Y-%m-%d %H:%M:%S')

    # Insert user
    dba_cursor = dba.cursor()
    dba_cursor.execute("INSERT INTO `users` (`id`, `username`, `email`, `password`, `date`) VALUES (%s, %s, %s, %s, %s)", (new_max_id, username, email, encrypted_password, date_time))
    dba_cursor.close()
    dba.commit()
    

def extract_visited_destinations_number(dba, user_id):
    """Function returns total number of visited destinations for a user based on user id
    """
    # Extract number
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT COUNT(*) FROM `visited_destinations` GROUP BY `user_id` HAVING `user_id`=%s", (user_id, ))
    visited_destinations_number = dba_cursor.fetchone()
    dba_cursor.close()

    # Case: no visited destinations
    if visited_destinations_number is None:
        return 0
    return visited_destinations_number[0]


def extract_wishlisted_destinations_number(dba, user_id):
    """Function returns total number of wishlisted destinatinos for a user based on user id
    """
    # Extract number
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT COUNT(*) FROM `wishlisted_destinations` GROUP BY `user_id` HAVING `user_id`=%s", (user_id, ))
    wishlisted_destinations_number = dba_cursor.fetchone()
    dba_cursor.close()

    # Case: no destinations on wishlist
    if wishlisted_destinations_number is None:
        return 0
    return wishlisted_destinations_number[0]


def extract_destinations_number(dba):
    """Function returns total number of destinations
    """
    # Extract total number
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT COUNT(*) FROM `destinations`")
    total_destinations_number = dba_cursor.fetchone()
    dba_cursor.close()
    return total_destinations_number[0]


def extract_visited_destinations_names(dba, user_id):
    """Function returns the names and the cover images of visited destinations for a user based on user id.

    It returns the destinations from the newest visited destination to the oldest visited destination.
    """
    # Extract names
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `d`.`name`, `d`.`image_link` FROM `destinations` `d` INNER JOIN `visited_destinations` `v` ON `d`.`id`=`v`.`destination_id` INNER JOIN `users` `u` ON `v`.`user_id` = `u`.`id` WHERE `u`.`id`=%s ORDER BY `v`.`date` DESC", (user_id, ))
    visited_destinations = dba_cursor.fetchall()
    dba_cursor.close()
    return visited_destinations


def extract_wishlisted_destinations_names(dba, user_id):
    """Function returns the names and the cover images of wishlisted destinations for a user based on user id.

    It returns the destinations from the newest wishlisted destination to the oldest wishlisted destination.
    """
    # Extract names
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `d`.`name`, `d`.`image_link` FROM `destinations` `d` INNER JOIN `wishlisted_destinations` `w` ON `d`.`id`=`w`.`destination_id` INNER JOIN `users` `u` ON `w`.`user_id` = `u`.`id` WHERE `u`.`id`=%s ORDER BY `w`.`date` DESC", (user_id, ))
    wishlisted_destinations = dba_cursor.fetchall()
    dba_cursor.close()
    return wishlisted_destinations


def extract_most_visited_destinations_names(dba):
    """Function returns the names and the cover images of most visited destinations.

    It returns the destinations in a decreasing order.
    """
    # Extract names
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `d`.`name`, `d`.`image_link`, COUNT(*) FROM `destinations` `d` JOIN `visited_destinations` `v` on `d`.`id` = `v`.`destination_id` GROUP BY `v`.`destination_id` ORDER BY COUNT(*) DESC LIMIT 4")
    most_visited_destinations = dba_cursor.fetchall()
    dba_cursor.close()
    return most_visited_destinations


def extract_most_reviewed_destinations_names(dba):
    """Function returns the names and the cover images of most reviewed destinations.

    It returns the destinations in a decreasing order.
    """
    # Extract names
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `d`.`name`, `d`.`image_link`, COUNT(*) FROM `destinations` `d` JOIN `reviews_destinations` `r` on `d`.`id` = `r`.`destination_id` GROUP BY `r`.`destination_id` ORDER BY COUNT(*) DESC LIMIT 4")
    most_reviewed_destinations = dba_cursor.fetchall()
    dba_cursor.close()
    return most_reviewed_destinations
    

def extract_destinations_names(dba):
    """Function returns the names and the cover images of all destinations available

    It returns the destinations in an order in which they are stored in the database.
    """
    # Extract names
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `name`, `image_link` FROM `destinations`")
    total_destinations = dba_cursor.fetchall()
    dba_cursor.close()
    return total_destinations
    

# Create database object
dba = connect_to_dba()