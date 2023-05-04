import mysql.connector
import time


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


def extract_user_for_login(dba, input_email: str, input_password: str):
    """Function returns user credentials (email and password) from database
    """
    # Extract user credentials
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `email`, `password` FROM `users` WHERE `email`=%s AND `password`=%s", (input_email, input_password))
    user_credentials = dba_cursor.fetchall()
    dba_cursor.close()
    return user_credentials


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


def extract_user_max_id(dba):
    """Function returns the biggest user id from database
    """
    # Extract maximum id number
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT MAX(`id`) from `users`")
    max_id = dba_cursor.fetchall()
    dba_cursor.close()
    return max_id


def insert_user(dba, username: str, email: str, password: str):
    """Function inserts user to the database
    """
    # Extract the biggest user id
    max_id = extract_user_max_id(dba)
    # Compute new user id
    new_max_id = max_id + 1

    # Extract date
    date_time = time.strftime('%Y-%m-%d %H:%M:%S')

    # Insert user
    dba_cursor = dba.cursor()
    dba_cursor.execute("INSERT INTO `users` (`id`, `username`, `email`, `password`, `date`) VALUES (%s, %s, %s, %s, %s)", (new_max_id, username, email, password, date_time))
    dba_cursor.close()
    dba.commit()


# Create database object
dba = connect_to_dba()