import sqlite3 as sql

filename = "./courses.db"

conn = sql.connect(filename)

cur = conn.cursor()

print("Connected to the database")

for row in cur.execute("SELECT * FROM courses"):
    print(row)