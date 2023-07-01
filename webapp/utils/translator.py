import translators as ts
import mysql.connector
import time
from utils_database import dba, extract_tourisitic_objectives_names, add_translated_name


# Extract names
names = extract_tourisitic_objectives_names(dba)

# Translate 30 names every 4 second
new_names = []
index = 0
for name in names:
    print("A ajuns la: ", name)
    new_names.append(ts.translate_text(name[0], translator="bing", to_language="en")) # type: ignore
    # Add touristic objective's translated name into the database
    add_translated_name(dba, str(names[index]), str(new_names[index]))
    index += 1
    if index == 20:
        index = 0
        time.sleep(5)