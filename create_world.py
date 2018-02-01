import os
import sqlite3
import sys

isDBExist=os.path.isfile('world.db')
DBCon=sqlite3.connect('world.db')

with DBCon:
    cursor=DBCon.cursor()
    if not isDBExist:  # First time creating the database. Create the tables
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
            count=1
            for line in config:
                myList=line.strip().split(",")
                if len(myList)==2:
                    cursor.execute("INSERT INTO resources VALUES(?,?)", (myList[0], myList[1]))
                elif len(myList)==3:
                    cursor.execute("INSERT INTO workers VALUES(?,?,?)", (myList[1], myList[2], "idle"))
                else:
                    cursor.execute("INSERT INTO tasks VALUES(?,?,?,?,?,?)",
                                   (count, myList[0], myList[1], myList[4], myList[2], myList[3]))
                    count+=1