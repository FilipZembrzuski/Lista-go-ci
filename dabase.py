import sqlite3 as sql
import os

db_Path = "lista_gości.db"

if os.path.exists(db_Path) != True:
    print("tworzę nową baze")
    open(db_Path, "x")
    conn = sql.connect(db_Path)
    conn.execute("CREATE TABLE `grupy` (`id` INT NOT NULL, `name` TEXT, PRIMARY KEY (`id`))")
    conn.execute("CREATE TABLE `goście` (`id` INT NOT NULL, `name` TEXT NOT NULL, `grupa` INT NOT NULL, `pod_grupa` INT NOT NULL, PRIMARY KEY (`id`))")
else:
    conn = sql.connect(db_Path)

def add_group(name):
    text = f"INSERT INTO `grupy`(`name`) VALUES ('{name}')"
    conn.execute(text)
    
def add_guest(name, group, ugroup):
    text = f"INSERT INTO `goście`(`name`,'grupa','podgrupa') VALUES ('{name}','{group}','{ugroup}')"
    conn.execute(text)


conn.commit()
conn.close()