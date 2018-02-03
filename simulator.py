import os
import sqlite3

isDBExist=os.path.isfile("world.db")
if not isDBExist:
    exit()
DBCon=sqlite3.connect("world.db")

with DBCon:
    cursor=DBCon.cursor()
    cursor.execute("SELECT id FROM workers")
    currentTask={i[0]: -1 for i in cursor.fetchall()}
    while True:
        cursor.execute("SELECT COUNT(ID) FROM tasks")
        if cursor.fetchone()[0]==0:
            break
        cursor.execute("SELECT * FROM tasks")
        tasks=cursor.fetchall()
        for task in tasks:
            cursor.execute("SELECT status, name FROM workers WHERE id=(?)", (task[2],))
            worker=cursor.fetchone()
            if worker[0]=="idle":
                currentTask[task[2]]=task[0]
                DBCon.execute("UPDATE workers SET status=(?) WHERE id=(?)", ("busy", task[2]))
                DBCon.execute("UPDATE resources SET amount=amount-(?) WHERE name=(?)", (task[5], task[4]))
                DBCon.execute("UPDATE tasks SET time_to_make=time_to_make-1 WHERE id=(?)", (task[0],))
                print("{} says: work work".format(worker[1]))

            # checks if the requested worker of this task is busy on this task
            elif currentTask[task[2]]==task[0]:
                if task[3]>=0:
                    DBCon.execute("UPDATE tasks SET time_to_make=time_to_make-1 WHERE id=(?)", (task[0],))
                    print("{} is busy {}...".format(worker[1], task[1]))
        for task in tasks:
            if task[3]==0:
                DBCon.execute("DELETE FROM tasks WHERE id=(?)", (task[0],))
                DBCon.execute("UPDATE workers SET status=(?) WHERE id=(?)", ("idle", task[2]))
                currentTask[task[2]]=-1
                cursor.execute("SELECT name FROM workers WHERE id=(?)", (task[2],))
                print("{} says: All Done!".format(cursor.fetchone()[0]))