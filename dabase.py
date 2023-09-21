import sqlite3 as sql
import os

dbPath = "lista_gości.db"

if os.path.exists(dbPath) != True:
    print("tworzę nową baze")
    f = open(dbPath, "x")
    f.close()
    conn = sql.connect(dbPath)
    conn.execute("""CREATE TABLE `groups` (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `name` TEXT, 'color' TEXT)""")
    conn.execute("""CREATE TABLE `guests` (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `name` TEXT NOT NULL, `group` INT NOT NULL, `u_group` INT NOT NULL)""")
    conn.execute("""Insert Into 'groups' ('name', 'color') Values ('rodzina','#ff00c9')""")
    conn.execute("""Insert Into 'groups' ('name', 'color') Values ('organizator','#ffffff')""")
    conn.commit()
else:
    conn = sql.connect(dbPath)

conn.close()