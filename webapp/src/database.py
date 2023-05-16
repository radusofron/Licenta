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
    

def extract_destinations_number(dba):
    """Function returns total number of destinations
    """
    # Extract total number
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT COUNT(*) FROM `destinations`")
    total_destinations = dba_cursor.fetchone()
    dba_cursor.close()
    return total_destinations[0]


def extract_wishlisted_destinations_number(dba, user_id):
    """Function returns total number of wishlisted destinatinos for a user based on user id
    """
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT COUNT(*) FROM `wishlisted_destinations` GROUP BY `user_id` HAVING `user_id`=%s", (user_id, ))
    wishlisted_destinations = dba_cursor.fetchone()
    dba_cursor.close()
    return wishlisted_destinations[0]


def extract_visited_destinations_number(dba, user_id):
    """Function returns total number of visited destinations for a user based on user id
    """
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT COUNT(*) FROM `visited_destinations` GROUP BY `user_id` HAVING `user_id`=%s", (user_id, ))
    visited_destinations = dba_cursor.fetchone()
    dba_cursor.close()
    return visited_destinations[0]


# Create database object
dba = connect_to_dba()