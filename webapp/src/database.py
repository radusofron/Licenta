import mysql.connector
import time
import datetime
from werkzeug.security import generate_password_hash, check_password_hash


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


def extract_the_three_most_visited_destinations(dba):
    """Function returns the three most visited destinations on the website.
    """
    # Extract destinations
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `d`.`name` FROM `destinations` `d` INNER JOIN `visited_destinations` `v` ON `d`.`id`=`v`.`destination_id` GROUP BY `destination_id` ORDER BY COUNT(*) DESC LIMIT 3")
    most_visited = dba_cursor.fetchall()
    dba_cursor.close()
    return most_visited


def extract_three_most_recent_website_reviews(dba):
    """Function returns the three most recent reviews about the website.
    """
    # Extract reviews
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `u`.`username`, `r`.`review` FROM `users` `u` INNER JOIN `reviews_website` `r` ON `u`.`id` = `r`.`user_id`  WHERE LENGTH(`r`.`review`) < 100 ORDER BY `r`.`date` DESC LIMIT 3")
    reviews = dba_cursor.fetchall()
    dba_cursor.close()
    return reviews


def login_validation(dba, input_email: str, input_password: str) -> bool:
    """Function returns login status.
    """
    # Extract user credentials
    email = extract_email(dba, input_email)
    if len(email) == 1:
        password = extract_user_password(dba, input_email)
        if check_password_hash(password[0][0], input_password):
            return True
    return False


def extract_user_id(dba, input_email: str):
    """Function returns user id from database based on email given.
    """
    # Extract id
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `id` FROM `users` WHERE `email`=%s", (input_email,))
    user_id = dba_cursor.fetchone()
    dba_cursor.close()
    return user_id[0]


def extract_username(dba, input_username: str):
    """Function returns username from database based on username given as input.

    Function used for register system.
    """
    # Extract username
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `username` FROM `users` WHERE `username`=%s", (input_username,))
    username = dba_cursor.fetchall()
    dba_cursor.close()
    return username


def extract_email(dba, input_email: str):
    """Function returns email from database based on email given as input.

    Function used for register and login systems.
    """
    # Extract email
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `email` FROM `users` WHERE `email`=%s", (input_email,))
    email = dba_cursor.fetchall()
    dba_cursor.close()
    return email


def extract_user_password(dba, input_email: str):
    """Function returns password from database based on email given as input.
    """
    # Extract password
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `password` FROM `users` WHERE `email`=%s", (input_email,))
    password = dba_cursor.fetchall()
    dba_cursor.close()
    return password


def extract_user_max_id(dba):
    """Function returns the biggest user id from database.
    """
    # Extract maximum id number
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT MAX(`id`) FROM `users`")
    max_id = dba_cursor.fetchone()
    dba_cursor.close()
    return max_id[0]


def insert_user(dba, username: str, email: str, password: str):
    """Function inserts an user into the database.
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

    # Traveler level
    traveler_level ="Novice"
    
    # Insert user
    dba_cursor = dba.cursor()
    dba_cursor.execute("INSERT INTO `users` (`id`, `username`, `email`, `password`, `date`, `traveler_level`) VALUES (%s, %s, %s, %s, %s, %s)", (new_max_id, username, email, encrypted_password, date_time, traveler_level))
    
    # Close cursor and commit changes
    dba_cursor.close()
    dba.commit()
    

def extract_visited_destinations_number(dba, user_id: int) -> int:
    """Function returns total number of visited destinations of a user based on user id.
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


def extract_wishlisted_destinations_number(dba, user_id: int) -> int:
    """Function returns total number of wishlisted destinatinos of a user based on user id.
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


def extract_destinations_number(dba) -> int:
    """Function returns total number of destinations.
    """
    # Extract total number
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT COUNT(*) FROM `destinations`")
    total_destinations_number = dba_cursor.fetchone()
    dba_cursor.close()
    return total_destinations_number[0]


def extract_visited_destinations_names(dba, user_id: int):
    """Function returns the names of visited destinations of a user based on user id starting with the newest added.
    """
    # Extract names
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `d`.`name` FROM `destinations` `d` INNER JOIN `visited_destinations` `v` ON `d`.`id`=`v`.`destination_id` INNER JOIN `users` `u` ON `v`.`user_id` = `u`.`id` WHERE `u`.`id`=%s ORDER BY `v`.`date` DESC", (user_id, ))
    visited_destinations = dba_cursor.fetchall()
    dba_cursor.close()
    return visited_destinations


def extract_wishlisted_destinations_names(dba, user_id: int):
    """Function returns the names of wishlisted destinations of a user based on user id starting with the newest added.
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
    """Function returns the names of all destinations available.

    It returns the destinations in an order in which they are stored in the database.
    """
    # Extract names
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `name` FROM `destinations`")
    total_destinations = dba_cursor.fetchall()
    dba_cursor.close()
    return total_destinations


def update_profile_picture_relative_path(dba, photo_name: str, user_id: int):
    """Function updates user's profile picture name to database.
    """
    # Update photo name
    dba_cursor = dba.cursor()
    dba_cursor.execute("UPDATE `users` SET `photo_name`=%s WHERE `id`=%s", (photo_name, user_id,))
    dba_cursor.close()
    dba.commit()


def extract_photo_name(dba, user_id: int):
    """Function returns user's profile picture name from database.
    """
    # Extract photo extension
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `photo_name` FROM `users` WHERE `id`=%s", (user_id,))
    photo_name = dba_cursor.fetchone()
    dba_cursor.close()
    
    # Case: photo name not found
    if photo_name[0] is None:
        return None
    return photo_name[0]


def extract_username_by_id(dba, user_id: int):
    """Function returns username based on id stored in session.
    """
    # Extract username
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `username` FROM `users` WHERE `id`=%s", (user_id,))
    username = dba_cursor.fetchone()
    dba_cursor.close()
    return username[0]


def extract_email_by_id(dba, user_id: int):
    """Function returns email based on id stored in session.
    """
    # Extract username
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `email` FROM `users` WHERE `id`=%s", (user_id,))
    email = dba_cursor.fetchone()
    dba_cursor.close()
    return email[0]


def extract_traveler_level_by_id(dba, user_id: int):
    """Function returns traveler level based on id stored in session.
    """
    # Extract traveler level
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `traveler_level` FROM `users` WHERE `id`=%s", (user_id,))
    traveler_level = dba_cursor.fetchone()
    dba_cursor.close()
    return traveler_level[0]


def extract_registration_date_by_id(dba, user_id: int):
    """Function returns registration date based on id stored in session.
    """
    # Extract username
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `date` FROM `users` WHERE `id`=%s", (user_id,))
    date = dba_cursor.fetchone()
    dba_cursor.close()
    return date[0]


def extract_visited_destinations_number_by_date(dba, year: int, user_id: int, option: int) -> int:
    """Function returns total number of visited destinations by a user based on user id and other parameters.

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

    # Case: no visited destinations found for correspondent option
    if visited_destinations_number is None:
        return 0
    return visited_destinations_number[0]


def extract_evaluated_destinations_number(dba, user_id: int) -> int:
    """Function returns total number of evaluated destinations by an user based on user id.
    """
    # Extract username
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT COUNT(*) FROM `grades_destinations` WHERE `user_id`=%s", (user_id,))
    evaluated_destinations_number = dba_cursor.fetchone()
    dba_cursor.close()
    
    # Case: no evaluated destinations found for user
    if evaluated_destinations_number is None:
        return 0
    return evaluated_destinations_number[0]


def extract_evaluated_destinations_total_grade(dba, user_id: int) -> list[tuple[int, int]]:
    """Function returns sum of the grades for every evaluated destinations by an user.
    """
    # Extract sums
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `destination_id`, (`grade_attractions` + `grade_acommodation` + `grade_culture` + `grade_entertainment` + `grade_food_and_drink` + `grade_history` + `grade_natural_beauty` + `grade_night_life` + `grade_transport` + `grade_safety`) FROM `grades_destinations` WHERE `user_id`=%s GROUP BY `destination_id`", (user_id,))
    evaluated_destinations_grades_sum = dba_cursor.fetchall()
    dba_cursor.close()
    return evaluated_destinations_grades_sum


def extract_destination_name_by_id(dba, destination_id: int) -> str:
    """Function returns destination's name for a given destination id.
    """
    # Extract average grades
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `name` FROM destinations WHERE `id`=%s", (destination_id,))
    destination_name = dba_cursor.fetchone()
    dba_cursor.close()
    
    # Case: no id returned
    if destination_name is None:
        return ""
    return destination_name[0]


def update_password(dba, new_password: str, user_id: int):
    """Function updates the password of an user in the database.
    """
    # Hash the password
    encrypted_new_password = generate_password_hash(new_password)

    # Update password
    dba_cursor = dba.cursor()
    dba_cursor.execute("UPDATE `users` SET `password`=%s WHERE `id`=%s", (encrypted_new_password, user_id))
    dba_cursor.close()
    dba.commit()


def delete_account_and_associated_data(dba, user_id: int):
    """Function deletes the account of an user from database.
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

    # 5. Delete data from travel itineraries table
    dba_cursor.execute("DELETE FROM `itineraries` WHERE user_id=%s;", (user_id,))

    # Close cursor and commit changes
    dba_cursor.close()
    dba.commit()


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


def extract_destination_average_grades(dba, destination_id: int) -> list[tuple]:
    """Function returns the average grades for a given destination id.
    """
    # Extract average grades
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT AVG(`grade_attractions`), AVG(`grade_acommodation`), AVG(`grade_culture`), AVG(`grade_entertainment`), AVG(`grade_food_and_drink`), AVG(`grade_history`), AVG(`grade_natural_beauty`), AVG(`grade_night_life`), AVG(`grade_transport`), AVG(`grade_safety`) FROM `grades_destinations` GROUP BY `destination_id` HAVING `destination_id`=%s", (destination_id,))
    average_grades = dba_cursor.fetchall()
    dba_cursor.close()

    # Case: no grades untill now
    if average_grades is None:
        return []
    return average_grades


def extract_destination_reviews(dba, destination_id: int) -> list[tuple]:
    """Function returns all the reviews for a given destiantion id, starting with the newest.
    """
    # Extract reviews
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `u`.`username`, `u`.`photo_name`, `r`.`date`, `u`.`traveler_level`, `r`.`feeling`, `r`.`review` FROM `users` `u` INNER JOIN `reviews_destinations` `r` ON `u`.`id` = `r`.`user_id` WHERE `r`.`destination_id`=%s ORDER BY `r`.`date` DESC", (destination_id,))
    reviews = dba_cursor.fetchall()
    dba_cursor.close()

    # Case: no reviews untill now
    if reviews is None:
        return []
    return reviews


def extract_max_id_from_wishlisted_destinations(dba):
    """Function returns maximum id from the wishlisted destinations table.
    """
    # Extract maximum id
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT MAX(`id`) FROM `wishlisted_destinations`")
    max_id = dba_cursor.fetchone()
    dba_cursor.close()
    return max_id[0]


def insert_wishlisted_destination_for_user(dba, user_id: int, destination_name: str):
    """Function inserts a wishlisted destination for an user into the database.
    """
    # Extract biggest id found in the table
    max_id = extract_max_id_from_wishlisted_destinations(dba)

    # Compute new id
    if max_id is None:
        # Case: first insertion
        new_max_id = 1
    else:
        # Case: the other insertions
        new_max_id = max_id + 1

    # Extract destination id
    destination_id = extract_destination_id_by_name(dba, destination_name)

    # Extract date
    date = time.strftime('%Y-%m-%d %H:%M:%S')

    # Open cursor
    dba_cursor = dba.cursor()

    # Insert wishlisted destinations   
    dba_cursor.execute("INSERT INTO `wishlisted_destinations` (`id`, `user_id`, `destination_id`, `date`) VALUES (%s, %s, %s, %s)", (new_max_id, user_id, destination_id, date))

    # Close cursor and commit changes
    dba_cursor.close()
    dba.commit()


def delete_wishlisted_destination_for_user(dba, user_id: int, destination_name: str):
    """Function deletes a wishlisted destination for an user from database.
    """
    # Extract destination id
    destination_id = extract_destination_id_by_name(dba, destination_name)

    # Open cursor
    dba_cursor = dba.cursor()

    # Delete wishlisted destination for user
    dba_cursor.execute("DELETE FROM `wishlisted_destinations` WHERE `user_id`=%s AND `destination_id`=%s;", (user_id, destination_id))

    # Close cursor and commit changes
    dba_cursor.close()
    dba.commit()


def extract_max_id_from_visited_destinations(dba):
    """Function returns maximum id from the visited destinations table.
    """
    # Extract maximum id
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT MAX(`id`) FROM `visited_destinations`")
    max_id = dba_cursor.fetchone()
    dba_cursor.close()
    return max_id[0]


def insert_visited_destination_for_user(dba, user_id: int, destination_name: str):
    """Function inserts a visited destination for an user into the database.
    """
    # Extract biggest id found in the table
    max_id = extract_max_id_from_visited_destinations(dba)

    # Compute new id
    if max_id is None:
        # Case: first insertion
        new_max_id = 1
    else:
        # Case: the other insertions
        new_max_id = max_id + 1

    # Extract destination id
    destination_id = extract_destination_id_by_name(dba, destination_name)

    # Extract date
    date = time.strftime('%Y-%m-%d %H:%M:%S')

    # Open cursor
    dba_cursor = dba.cursor()

    # Insert visited destinations   
    dba_cursor.execute("INSERT INTO `visited_destinations` (`id`, `user_id`, `destination_id`, `date`) VALUES (%s, %s, %s, %s)", (new_max_id, user_id, destination_id, date))

    # Close cursor and commit changes
    dba_cursor.close()
    dba.commit()


def delete_visited_destination_for_user(dba, user_id: int, destination_name: str):
    """Function deletes a visited destination for an user from database.
    """
    # Extract destination id
    destination_id = extract_destination_id_by_name(dba, destination_name)

    # Open cursor
    dba_cursor = dba.cursor()

    # Delete visited destination for user
    dba_cursor.execute("DELETE FROM `visited_destinations` WHERE `user_id`=%s AND `destination_id`=%s", (user_id, destination_id))

    # Delete evaluation done by the user
    dba_cursor.execute("DELETE FROM `grades_destinations` WHERE `user_id`=%s AND `destination_id`=%s", (user_id, destination_id))

    # Delete review given by the user 
    dba_cursor.execute("DELETE FROM `reviews_destinations` WHERE `user_id`=%s AND `destination_id`=%s", (user_id, destination_id))
    
    # Close cursor and commit changes
    dba_cursor.close()
    dba.commit()


def update_traveler_level_for_user(dba, user_id: int, traveler_level: str):
    """Function updates traveler level for an user into the database.
    """
    # Open cursor
    dba_cursor = dba.cursor()

    # Insert visited destinations   
    dba_cursor.execute("UPDATE `users` SET `traveler_level`=%s WHERE `id`=%s", (traveler_level, user_id))

    # Close cursor and commit changes
    dba_cursor.close()
    dba.commit()


def extract_visited_destination_date_for_user(dba, user_id: int, destination_name: str):
    """Function returns the date when the destination was visited by the user.
    """
    # Extract destination id
    destination_id = extract_destination_id_by_name(dba, destination_name)
    
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `date` FROM `visited_destinations` WHERE `user_id`=%s AND `destination_id`=%s", (user_id, destination_id))
    visited_date = dba_cursor.fetchone()
    dba_cursor.close()

    return visited_date[0]


def extract_max_id_from_grades_destinations(dba):
    """Function returns maximum id from the grades destinations table.
    """
    # Extract maximum id
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT MAX(`id`) FROM `grades_destinations`")
    max_id = dba_cursor.fetchone()
    dba_cursor.close()
    return max_id[0]


def insert_visited_destination_evaluation_by_user(dba, user_id: int, destination_name: str, grades: list):
    """Function inserts the grades given by an user for a visited destination into the database.
    """
    # Extract biggest id found in the table
    max_id = extract_max_id_from_grades_destinations(dba)

    # Compute new id
    if max_id is None:
        # Case: first insertion
        new_max_id = 1
    else:
        # Case: the other insertions
        new_max_id = max_id + 1

    # Extract destination id
    destination_id = extract_destination_id_by_name(dba, destination_name)

    # Extract date
    date = time.strftime('%Y-%m-%d %H:%M:%S')

    # Open cursor
    dba_cursor = dba.cursor()

    # Insert evaluation   
    dba_cursor.execute("INSERT INTO `grades_destinations` (`id`, `user_id`, `destination_id`, `grade_attractions`, `grade_acommodation`, `grade_culture`, `grade_entertainment`, `grade_food_and_drink`, `grade_history`, `grade_natural_beauty`, `grade_night_life`, `grade_transport`, `grade_safety`, `date`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (new_max_id, user_id, destination_id, grades[0], grades[1], grades[2], grades[3], grades[4], grades[5], grades[6], grades[7], grades[8], grades[9], date))

    # Close cursor and commit changes
    dba_cursor.close()
    dba.commit()


def extract_visited_destination_evaluation_by_user(dba, user_id: int, destination_name: str):
    """Function returns the grades given by an user for a visited destination from the database.
    """
    # Extract destination id
    destination_id = extract_destination_id_by_name(dba, destination_name)

    # Extract grades
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `grade_attractions`, `grade_acommodation`, `grade_culture`, `grade_entertainment`, `grade_food_and_drink`, `grade_history`, `grade_natural_beauty`, `grade_night_life`, `grade_transport`, `grade_safety` FROM `grades_destinations` WHERE `user_id`=%s AND `destination_id`=%s", (user_id, destination_id))
    grades = dba_cursor.fetchone()
    dba_cursor.close()

    # Case: no evaluation found
    if grades is None:
        return tuple()

    return grades


def update_visited_destination_evaluation_by_user(dba, user_id: int, destination_name: str, grades: list):
    """Function updates the grades given by an user for a visited destination into the database.
    """
    # Extract destination id
    destination_id = extract_destination_id_by_name(dba, destination_name)

    # Extract date
    date = time.strftime('%Y-%m-%d %H:%M:%S')

    # Open cursor
    dba_cursor = dba.cursor()

    # Update evaluation   
    dba_cursor.execute("UPDATE `grades_destinations` SET `grade_attractions`=%s, `grade_acommodation`=%s, `grade_culture`=%s, `grade_entertainment`=%s, `grade_food_and_drink`=%s, `grade_history`=%s, `grade_natural_beauty`=%s, `grade_night_life`=%s, `grade_transport`=%s, `grade_safety`=%s, `date`=%s WHERE `user_id`=%s AND `destination_id`=%s", (grades[0], grades[1], grades[2], grades[3], grades[4], grades[5], grades[6], grades[7], grades[8], grades[9], date, user_id, destination_id))

    # Close cursor and commit changes
    dba_cursor.close()
    dba.commit()


def extract_max_id_from_reviews_destinations(dba):
    """Function returns maximum id from the reviews destinations table.
    """
    # Extract maximum id
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT MAX(`id`) FROM `reviews_destinations`")
    max_id = dba_cursor.fetchone()
    dba_cursor.close()
    return max_id[0]


def insert_visited_destination_review_by_user(dba, user_id: int, destination_name: str, review: str, general_feeling: str):
    """Function inserts the review given by an user for a visited destination into the database.
    """
    # Extract biggest id found in the table
    max_id = extract_max_id_from_reviews_destinations(dba)

    # Compute new id
    if max_id is None:
        # Case: first insertion
        new_max_id = 1
    else:
        # Case: the other insertions
        new_max_id = max_id + 1

    # Extract destination id
    destination_id = extract_destination_id_by_name(dba, destination_name)

    # Extract date
    date = time.strftime('%Y-%m-%d %H:%M:%S')

    # Open cursor
    dba_cursor = dba.cursor()

    # Insert review   
    dba_cursor.execute("INSERT INTO `reviews_destinations` (`id`, `user_id`, `destination_id`, `review`, `feeling`, `date`) VALUES (%s, %s, %s, %s, %s, %s)", (new_max_id, user_id, destination_id, review, general_feeling, date))

    # Close cursor and commit changes
    dba_cursor.close()
    dba.commit()


def extract_visited_destination_review_by_user(dba, user_id: int, destination_name: str):
    """Function returns the review given by an user for a visited destination from the database.
    """
    # Extract destination id
    destination_id = extract_destination_id_by_name(dba, destination_name)

    # Extract review
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `review` FROM `reviews_destinations` WHERE `user_id`=%s AND `destination_id`=%s", (user_id, destination_id))
    review = dba_cursor.fetchone()
    dba_cursor.close()

    # Case: no review found
    if review is None:
        return ""
    return review[0]


def update_visited_destination_review_by_user(dba, user_id: int, destination_name: str, review: str):
    """Function updates the review given by an user for a visited destination into the database.
    """
    # Extract destination id
    destination_id = extract_destination_id_by_name(dba, destination_name)

    # Extract date
    date = time.strftime('%Y-%m-%d %H:%M:%S')

    # Open cursor
    dba_cursor = dba.cursor()

    # Update review   
    dba_cursor.execute("UPDATE `reviews_destinations` SET `review`=%s, `date`=%s WHERE `user_id`=%s AND `destination_id`=%s", (review, date, user_id, destination_id))

    # Close cursor and commit changes
    dba_cursor.close()
    dba.commit()


def extract_touristic_objectives_names(dba, destination_name: str):
    """Function returns the touristic objectives' names and details of a destination from database.
    """
    # Extract destination id
    destination_id = extract_destination_id_by_name(dba, destination_name)
    
    # Extract touristic objectives
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `name` FROM `touristic_objectives` WHERE destination_id=%s", (destination_id,))
    touristic_objectives = dba_cursor.fetchall()
    dba_cursor.close()

    return touristic_objectives


def extract_touristic_objective_coordinates_by_name(dba, objective_name: str):
    """Function returns the coordinates of a touristic objective from database.
    """
    # Extract coordinates
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `name`, `longitude`, `latitude` FROM `touristic_objectives` WHERE `name`=%s", (objective_name,))
    coordinates = dba_cursor.fetchall()
    dba_cursor.close()

    return coordinates


def insert_itinerary_for_user(dba, itinerary: dict, user_id: int, destiantion_name: str, objectives_groups: dict):
    """Function inserts a travel itinerary for an user into the database.
    """
    # Extract destination id
    destination_id = extract_destination_id_by_name(dba, destiantion_name)

    # Extract date
    date = time.strftime('%Y-%m-%d %H:%M:%S')

    # Open cursor
    dba_cursor = dba.cursor()

    # Insert itinerary   
    dba_cursor.execute("INSERT INTO `itineraries` (`id`, `name`, `description`, `user_id`, `destination_id`, `day1`, `day2`, `day3`, `day4`, `day5`, `day6`, `day7`, `date`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (itinerary["id"], itinerary["name"], itinerary["description"], user_id, destination_id, objectives_groups["day1"], objectives_groups["day2"], objectives_groups["day3"], objectives_groups["day4"], objectives_groups["day5"], objectives_groups["day6"], objectives_groups["day7"], date))

    # Close cursor and commit changes
    dba_cursor.close()
    dba.commit()


def extract_itineraries_id(dba, user_id: int):
    """Function returns the ids of all the travel itineraries of an user.
    """
    # Extract travel itineraries ids
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `id` FROM `itineraries` WHERE `user_id`=%s", (user_id,))
    itineraries_ids = dba_cursor.fetchall()
    dba_cursor.close()

    return itineraries_ids


def extract_itineraries_main_details(dba, user_id: int):
    """Function returns the ids, names, for which cities and dates of all the travel itineraries of an user.
    """
    # Extract travel itineraries ids, names, dates
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT `id`, `name`, `destination_id`, `date` FROM `itineraries` WHERE `user_id`=%s ORDER BY `date` DESC", (user_id,))
    itineraries_main_details = dba_cursor.fetchall()
    dba_cursor.close()

    return itineraries_main_details


def extract_itinerary(dba, user_id: int, itinerary_id: str):
    """Function returns a specific itinerary of an user based on its id from database.
    """
    # Extract itinerary
    dba_cursor = dba.cursor()
    dba_cursor.execute("SELECT * FROM `itineraries` WHERE `user_id`=%s AND `id`=%s", (user_id, itinerary_id))
    itinerary = dba_cursor.fetchone()
    dba_cursor.close()

    return itinerary


def extract_touristic_objectives_details_by_name(dba, objective_name: str):
    """Function returns the details of a touristic objective from database.
    """
    # Extract details
    dba_cursor = dba.cursor(buffered = True)
    dba_cursor.execute("SELECT `address`, `opening_hours` FROM `touristic_objectives` WHERE `name`=%s", (objective_name,))
    details = dba_cursor.fetchone()
    dba_cursor.close()

    return details

def delete_itinerary_for_user(dba, itinerary_id: str):
    """Function deletes a travel itinerary for an user from database.
    """
    # Open cursor
    dba_cursor = dba.cursor()

    # Delete visited destination for user
    dba_cursor.execute("DELETE FROM `itineraries` WHERE `id`=%s", (itinerary_id, ))
    
    # Close cursor and commit changes
    dba_cursor.close()
    dba.commit()


# Create database object
dba = connect_to_dba()