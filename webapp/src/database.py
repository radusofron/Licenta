import mysql.connector


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


def extract_user(dba, input_email: str, input_password: str):
    """Function returns user from database
    """
    # Extract user credentials
    dba_cursor = dba.cursor()
    dba_cursor.execute(f"SELECT `email`, `password` FROM `users` WHERE `email`=%s AND `password`=%s", (input_email, input_password))
    user_credentials = dba_cursor.fetchall()
    return user_credentials


# TODO -> cand exista deja un cont cu email-ul dat
# TODO -> cand exista deja un cont cu username-ul dat
# TODO -> cand se trece de verificarile mai sus, se insereaza


# Create database object
dba = connect_to_dba()