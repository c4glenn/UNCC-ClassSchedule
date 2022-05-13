from io import StringIO
import json
import sqlite3 as sql
import os

filename = "./courses.db"

if os.path.exists(filename):
    os.remove(filename)


conn = sql.connect(filename)

cur = conn.cursor()

print("Connected to the database")

createTableCommand = """CREATE TABLE courses(
    coid INT PRIMARY KEY,
    code TEXT,
    title TEXT,
    description TEXT,
    hours INT,
    restrictions TEXT,
    prereqs TEXT);"""
    
cur.execute(createTableCommand)

io = StringIO()

with open("./courses.json", "r") as f:
    courseList = json.loads(f.read())
    i = 0
    for course in courseList:
        print(i)
        i +=1
        cur.execute(f"INSERT INTO courses VALUES (?,?,?,?,?,?,?)", (course["coid"] , "'" + str(course["code"]) + "'" , "'" + str(course["title"]) + "'", "'" + str(course["description"]) + "'", course["hours"], "'" + str(course["restrictions"]) + "'", "'" + str(json.dump(course["prerequisits"], io)) + "'"))

conn.close()
