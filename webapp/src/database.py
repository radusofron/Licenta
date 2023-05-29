import mysql.connector
import time
import datetime
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
    email = extract_email(dba, input_email)
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


def extract_username(dba, input_username: str):
    """Function returns username from database based on username given as input

    Function used for register system.
    """
    # Extract username
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `username` FROM `users` WHERE `username`=%s", (input_username,))
    username = dba_cursor.fetchall()
    dba_cursor.close()
    return username


def extract_email(dba, input_email: str):
    """Function returns email from database based on email given as input

    Function used for register and login systems.
    """
    # Extract email
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `email` FROM `users` WHERE `email`=%s", (input_email,))
    email = dba_cursor.fetchall()
    dba_cursor.close()
    return email


def extract_user_password(dba, input_email: str):
    """Function returns password from database based on email given as input
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
    """Function inserts user to database.
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
    """Function returns the names of visited destinations for a user based on user id.

    It returns the destinations from the newest visited destination to the oldest visited destination.
    """
    # Extract names
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `d`.`name` FROM `destinations` `d` INNER JOIN `visited_destinations` `v` ON `d`.`id`=`v`.`destination_id` INNER JOIN `users` `u` ON `v`.`user_id` = `u`.`id` WHERE `u`.`id`=%s ORDER BY `v`.`date` DESC", (user_id, ))
    visited_destinations = dba_cursor.fetchall()
    dba_cursor.close()
    return visited_destinations


def extract_wishlisted_destinations_names(dba, user_id):
    """Function returns the names of wishlisted destinations for a user based on user id.

    It returns the destinations from the newest wishlisted destination to the oldest wishlisted destination.
    """
    # Extract names
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `d`.`name` FROM `destinations` `d` INNER JOIN `wishlisted_destinations` `w` ON `d`.`id`=`w`.`destination_id` INNER JOIN `users` `u` ON `w`.`user_id` = `u`.`id` WHERE `u`.`id`=%s ORDER BY `w`.`date` DESC", (user_id, ))
    wishlisted_destinations = dba_cursor.fetchall()
    dba_cursor.close()
    return wishlisted_destinations


def extract_most_visited_destinations_names(dba):
    """Function returns the names of most visited destinations.

    It returns the destinations in a decreasing order.
    """
    # Extract names
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `d`.`name`, COUNT(*) FROM `destinations` `d` JOIN `visited_destinations` `v` on `d`.`id` = `v`.`destination_id` GROUP BY `v`.`destination_id` ORDER BY COUNT(*) DESC LIMIT 4")
    most_visited_destinations = dba_cursor.fetchall()
    dba_cursor.close()
    return most_visited_destinations


def extract_most_reviewed_destinations_names(dba):
    """Function returns the names of most reviewed destinations.

    It returns the destinations in a decreasing order.
    """
    # Extract names
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `d`.`name`, COUNT(*) FROM `destinations` `d` JOIN `reviews_destinations` `r` on `d`.`id` = `r`.`destination_id` GROUP BY `r`.`destination_id` ORDER BY COUNT(*) DESC LIMIT 4")
    most_reviewed_destinations = dba_cursor.fetchall()
    dba_cursor.close()
    return most_reviewed_destinations
    

def extract_destinations_names(dba):
    """Function returns the names of all destinations available

    It returns the destinations in an order in which they are stored in the database.
    """
    # Extract names
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `name` FROM `destinations`")
    total_destinations = dba_cursor.fetchall()
    dba_cursor.close()
    return total_destinations


def update_photo_relative_path(dba, relative_path, user_id):
    """Function updates user's profile picture extension to database.
    """
    # Update photo extension
    dba_cursor = dba.cursor()
    dba_cursor.execute("UPDATE `users` SET `photo_path`=%s WHERE `id`=%s", (relative_path, user_id,))
    dba_cursor.close()
    dba.commit()


def extract_photo_relative_path(dba, user_id):
    """Function returns user's profile picture relative path from database.
    
    Function returns an empty list if no profile picture was uploaded before.
    """
    # Extract photo extension
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `photo_path` FROM `users` WHERE `id`=%s", (user_id,))
    relative_path = dba_cursor.fetchone()
    dba_cursor.close()
    return relative_path


def extract_username_by_id(dba, user_id):
    """Function returns username, email and registration date based on id stored in session.
    """
    # Extract username
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `username` FROM `users` WHERE `id`=%s", (user_id,))
    username = dba_cursor.fetchone()
    dba_cursor.close()
    return username[0]


def extract_email_by_id(dba, user_id):
    """Function returns username, email and registration date based on id stored in session.
    """
    # Extract username
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `email` FROM `users` WHERE `id`=%s", (user_id,))
    email = dba_cursor.fetchone()
    dba_cursor.close()
    return email[0]


def extract_registration_date_by_id(dba, user_id):
    """Function returns username, email and registration date based on id stored in session.
    """
    # Extract username
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `date` FROM `users` WHERE `id`=%s", (user_id,))
    date = dba_cursor.fetchone()
    dba_cursor.close()
    return date[0]


def extract_visited_destinations_number_by_date(dba, year: int, user_id: int, option: int):
    """Function returns total number of visited destinations for a user based on user id.

    Parameters:
        * dba: database object
        * year: year used in the query
        * option: function proceeds accordingly based on the selected option; 
        if option is 1, it returns total number of visited destinations from the year given untill now;
        if option is 2, it returns total number of visited destinations in that year
    """

    if option == 1:
        # First, compute the starting date to be used

        # Create starting date
        start_date = datetime.datetime(year, 1, 1)

        # Convert starting date to specific format (string)
        start_date = start_date.strftime('%Y-%m-%d %H:%M:%S')

        # Extract number
        dba_cursor = dba.cursor()
        dba_cursor.execute("SELECT COUNT(*) FROM `visited_destinations` WHERE `date`>%s AND `user_id`=%s", (start_date, user_id))
        visited_destinations_number = dba_cursor.fetchone()
        dba_cursor.close()
    else:
        # Extract number
        dba_cursor = dba.cursor()
        dba_cursor.execute("SELECT COUNT(*) FROM `visited_destinations` WHERE YEAR(`date`)=%s AND `user_id`=%s", (year, user_id))
        visited_destinations_number = dba_cursor.fetchone()
        dba_cursor.close()

    # Case: no visited destinations from starting date unitll now
    if visited_destinations_number is None:
        return 0
    return visited_destinations_number[0]


def update_password(dba, new_password: str, user_id: int):
    """Function updates user's password.
    """
    # Hash the password
    encrypted_new_password = generate_password_hash(new_password)

    # Update password
    dba_cursor = dba.cursor()
    dba_cursor.execute("UPDATE `users` SET `password`=%s WHERE `id`=%s", (encrypted_new_password, user_id))
    dba_cursor.close()
    dba.commit()


def delete_account_and_associated_data(dba, user_id: int):
    """Function deletes user's account.
    """
    # Open cursor
    dba_cursor = dba.cursor()

    # 1. Delete data from users table
    dba_cursor.execute("DELETE FROM `users` WHERE id=%s;", (user_id,))

    # 2. Delete data from visited destinations table
    dba_cursor.execute("DELETE FROM `visited_destinations` WHERE user_id=%s;", (user_id,))
    
    # 3. Delete data from wishlisted destinations table
    dba_cursor.execute("DELETE FROM `wishlisted_destinations` WHERE user_id=%s;", (user_id,))
    
    # 4. Delete data from reviews destinations table
    dba_cursor.execute("DELETE FROM `reviews_destinations` WHERE user_id=%s;", (user_id,))

    # TODO 5. Delete data from travel itineraries table / json file

    # Close cursor and commit changes
    dba_cursor.close()
    dba.commit()
    

# Create database object
dba = connect_to_dba()