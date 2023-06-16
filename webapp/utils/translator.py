import translators as ts
import mysql.connector
import time


dba_host = 'localhost'
dba_user = 'radu'
dba_password = 'mysqlradu'
dba_name = 'travel_with_us'

# Connect to database
dba = mysql.connector.connect(host=dba_host, password=dba_password, user=dba_user, database=dba_name)

dba_cursor = dba.cursor()
dba_cursor.execute("SELECT `name` FROM `touristic_objectives`")
words = dba_cursor.fetchall()
dba_cursor.close()
print(words)

index = 0
for word in words:
    print(ts.translate_text(word[0], translator="bing", to_language="en")) # type: ignore
    index += 1
    if index == 30:
        index = 0
        time.sleep(5)