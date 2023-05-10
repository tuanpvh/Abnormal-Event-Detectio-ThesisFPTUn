import sqlite3
connection = sqlite3.connect("Db_Doan1.db")
cursor = connection.cursor()

sql_file = open("sample.sql")
sql_as_string = sql_file.read()
cursor.executescript(sql_as_string)

for row in cursor.execute("SELECT * FROM User"):
    print(row)