import sqlite3
import os
import sys

databaseexisted = os.path.isfile('world.db')

dbcon = sqlite3.connect('world.db')

with dbcon:
    cursor = dbcon.cursor()
    if not databaseexisted:  # First time creating the database. Create the tables
        cursor.execute("CREATE TABLE tasks("
                       "ID INTEGER PRIMARY KEY,"
                       "task_name TEXT NOT NULL,"
                       "worker_id INTEGER REFERENCES workers(id),"
                       "time_to_make INTEGER NOT NULL,"
                       "resource_name TEXT NOT NULL,"
                       "resource_amount INTEGER NOT NULL)")

        cursor.execute("CREATE TABLE workers("
                       "id INTEGER PRIMARY KEY,"
                       "name TEXT NOT NULL,"
                       "status TEXT NOT NULL)")

        cursor.execute("CREATE TABLE resources("
                       "name TEXT PRIMARY KEY,"
                       "amount INTEGER NOT NULL)")

        with open(sys.argv[1]) as config:
            count = 1
            for line in config:
                mylist = line.strip().split(",")
                if len(mylist) == 2:
                    cursor.execute("INSERT INTO resources VALUES(?,?)", (mylist[0], mylist[1]), )
                elif len(mylist) == 3:
                    cursor.execute("INSERT INTO workers VALUES(?,?,?)", (mylist[1], mylist[2], "idle"))
                else:
                    cursor.execute("INSERT INTO tasks VALUES(?,?,?,?,?,?)",
                                   (count, mylist[0], mylist[1], mylist[4], mylist[2], mylist[3]))
                    count += 1