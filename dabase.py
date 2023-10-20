import sqlite3 as sql
import os

dbPath = "lista_gości.db"

if os.path.exists(dbPath) != True:
    f = open(dbPath, "x")
    f.close()
    conn = sql.connect(dbPath)
    conn.execute("""CREATE TABLE `lists` (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `name` TEXT, disable integer)""")
    conn.execute("""CREATE TABLE `groups` (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `name` TEXT, 'color' TEXT, 'table_id' INTEGER)""")
    conn.commit()
else:
    conn = sql.connect(dbPath)
conn.commit()

conn.close()