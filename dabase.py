import sqlite3 as sql
import os

dbPath = "lista_gości.db"

if os.path.exists(dbPath) != True:
    f = open(dbPath, "x")
    f.close()
    conn = sql.connect(dbPath)
    conn.execute("""CREATE TABLE `groups` (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `name` TEXT, 'color' TEXT)""")
    conn.execute("""CREATE TABLE `guests` (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `name` TEXT NOT NULL, `group` INT NOT NULL, `u_group` INT NOT NULL, `active` BOOL NOT NULL)""")
    conn.commit()
else:
    conn = sql.connect(dbPath)

conn.commit()

conn.close()