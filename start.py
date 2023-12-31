from flask import Flask, render_template, request, redirect, url_for
import dabase
import sqlite3 as sql

app = Flask(__name__)
    
def add_group(name, color, tid):
    conn = sql.connect("lista_gości.db")
    conn.execute(f"""Insert Into 'groups' ('name', 'color', 'table_id') VALUES ('{name}', '{color}', {tid})""")
    conn.commit()
    conn.close()
    
def add_element(lista, name, group, ugroup):
    conn = sql.connect("lista_gości.db")
    addElement = f"INSERT INTO `{lista}`(`name`,'group','u_group','active') VALUES ('{name}','{group}','{ugroup}',True)"
    conn.execute(addElement)
    conn.commit()
    conn.close()
    
def select_group(id):
    conn = sql.connect("lista_gości.db")
    selectGroups = f"Select id, name, color From `groups` Where `table_id` = {id}"
    cursor = conn.execute(selectGroups)
    conn.commit()
    
    groups = []
    for g in cursor:
        group = {
            'id': g[0],
            'name':g[1],
            'color':g[2]
        }
        groups.append(group)
        
    conn.close()
    return(groups)

def select_ugroup(lista):
    conn = sql.connect("lista_gości.db")
    select_ugroups = f"Select id, name From `{lista}` Where u_group = 0 "
    cursor = conn.execute(select_ugroups)
    conn.commit()
    
    ugroups = []
    for u in cursor:
        ugroup = {
            'id':u[0],
            'name': u[1]
        }
        ugroups.append(ugroup)
        
    conn.close()
    return(ugroups)

def select_elements(nazwa, id):
    conn = sql.connect("lista_gości.db")
    selectElements = f"Select id, `name`, `group`, `u_group`, `active` From `{nazwa}` Order by `group` asc;"
    selectColors = f"Select id, color From `groups` where `table_id` = {id}"
    cursor = conn.execute(selectElements)
    cursor2 = conn.execute(selectColors)
    conn.commit()
    
    colors = {}
    for c in cursor2:
        colors[str(c[0])] = str(c[1])
        print(str(c[0]) + " : " + c[1])
    elements = []
    for g in cursor:
        element = {
            'id':g[0],
            'name':g[1],
            'group':g[2],
            'u_group':g[3],
            'status':g[4],
            'color':colors[str(g[2])]
        }
        elements.append(element)
    
    conn.close()
    return(elements)

def disctive_element(id):
    conn = sql.connect("lista_gości.db")
    dezactiveElement = f"UPDATE `guests` SET active = FALSE WHERE `id` = {id}"
    conn.execute(dezactiveElement)
    conn.commit()
    conn.close()
    
def reactive_element(id, lista):
    conn = sql.connect("lista_gości.db")
    dezactiveGroup = f"UPDATE `{lista}` SET active = TRUE WHERE `id` = {id}"
    conn.execute(dezactiveGroup)
    conn.commit()
    conn.close()
    
def del_group(id):
    conn = sql.connect("lista_gości.db")
    deleteGroup = f"DELETE FROM `groups` WHERE `id` = {id};"
    conn.execute(deleteGroup)
    conn.commit()
    conn.close()

def del_element(id, list):
    conn = sql.connect("lista_gości.db")
    deleteList = f"DELETE FROM `{list}` WHERE `id` = {id};"
    conn.execute(deleteList)
    conn.commit()
    conn.close()

def edit_groups(id, color):
    conn = sql.connect("lista_gości.db")
    updateGroup = f"UPDATE `groups` SET color='{color}' WHERE `id` = {id}"
    conn.execute(updateGroup)
    conn.commit()
    conn.close()
    
def add_list(name):
    conn = sql.connect("lista_gości.db")
    addTable = f"CREATE TABLE `{name}` (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `name` TEXT NOT NULL, `group` INT NOT NULL, `u_group` INT NOT NULL, `active` BOOL NOT NULL)"
    addList = f"INSERT INTO `lists`(`name`) VALUES ('{name}')"
    conn.execute(addTable)
    conn.execute(addList)
    conn.commit()
    conn.close()

def select_list():
    conn = sql.connect("lista_gości.db")
    selectList = f"Select id, name, disable From `lists`"
    cursor = conn.execute(selectList)
    conn.commit()
    
    lists = []
    for l in cursor:
        list = {
            'id': l[0],
            'name':l[1],
            'status':l[2]
        }
        lists.append(list)
        
    conn.close()
    return(lists)

def del_list(id, name):
    conn = sql.connect("lista_gości.db")
    deleteList = f"DELETE FROM `lists` WHERE `id` = {id};"
    deleteTable = f"Drop Table {name};"
    conn.execute(deleteList)
    conn.execute(deleteTable)
    conn.commit()
    conn.close()

def edit_list(id, name):
    conn = sql.connect("lista_gości.db")
    updateList = f"UPDATE `lists` SET name='{name}' WHERE `id` = {id}"
    conn.execute(updateList)
    conn.commit()
    conn.close()
    
@app.route("/home", methods = ['GET'])
@app.route("/", methods = ['GET'])
@app.route("/show_list", methods = ['POST', 'GET'])
def show_list():
    lists = select_list()
    if request.method == "GET":
        for l in lists:
            if l["id"] > 0:
                nazwa = l["name"]
                id = l["id"]
                elements = select_elements(nazwa, id)
                break
            else: 
                elements = []
    elif request.method == "POST":
        nazwa = request.form["name"]
        id = request.form["id"]
        elements = select_elements(nazwa, id)
    return render_template("list.html", lists = lists, el = elements, count = len(elements), nazwa = nazwa)

@app.route("/add_element", methods = ['POST', 'GET'])
def add_elements():
    lists = select_list()
    if request.method == "GET":
        for l in lists:
            if l["id"] > 0:
                nazwa = l["name"]
                id = l["id"]
                groups = select_group(id)
                ugroups = select_ugroup(nazwa)
                break
            else: 
                nazwa = "none"
                id = 0
                groups = []
                ugroups = []
    elif request.method == "POST":
        nazwa = request.form["name"]
        for l in lists:
            if l["name"] == nazwa:
                id = l["id"]
                break
            else: 
                id = 0
        groups = select_group(id)
        ugroups = select_ugroup(nazwa)
    
    return render_template("add_element.html", lists = lists, groups = groups, ugroups = ugroups, nazwa = nazwa, id = id)

@app.route("/new_element", methods = ['POST'])
def new_element():
    if request.method == "POST":
        lista = request.form["name"]
        name = request.form['ename']
        group = request.form['egroup']
        ugroup = request.form['eugroup']
        add_element(lista, name, group, ugroup)
        return redirect("/add_element", code=302)
    else:
        return redirect("/add_element", code=302)
    
@app.route("/new_group", methods = ['POST'])
def new_group():
    if request.method == "POST":
        name = request.form['gname']
        color = request.form['gcolor']
        lid = request.form["lid"]
        add_group(name, color, lid)
    return redirect("/add_element", code=302)

@app.route("/delete_group", methods = ['POST'])
def delete_group():
    if request.method == "POST":
        id = request.form['gid']
        del_group(id)
        return redirect("/add_element", code=302)
    
@app.route("/delete_element", methods = ['POST'])
def delete_element():
    if request.method == "POST":
        id = request.form['eid']
        stat = request.form['stat']
        lista = request.form['list']
        if stat == "1":
            disctive_element(id)
        else:
            del_element(id, lista)
        return redirect("/", code=302)
    
@app.route("/reload_element", methods = ['POST'])
def reload_element():
    if request.method == "POST":
        lista = request.form['list']
        id = request.form['eid']
        reactive_element(id, lista)
        return redirect("/", code=302)
    
@app.route("/edit_group", methods = ['POST'])
def update_group():
    if request.method == "POST":
        id = request.form['gid']
        color = request.form['ucolor']
        edit_groups(id, color)
        return redirect("/add_element", code=302)
    
@app.route("/add_list")
def select_lists():
    lists = select_list()
    return render_template("add_list.html", lists = lists, count = len(lists))

@app.route("/new_list", methods = ['POST'])
def add_lists():
    if request.method == "POST":
        name = request.form['name']
        add_list(name)
        return redirect("/add_list", code=302)

@app.route("/drop_list", methods = ['POST'])
def drop_lists():
    if request.method == "POST":
        id = request.form['lid']
        name = request.form['name']
        del_list(id, name)
        return redirect("/add_list", code=302)

@app.route("/edit_list", methods = ['POST'])
def edit_lists():
    if request.method == "POST":
        id = request.form['lid']
        name = request.form['name']
        edit_list(id, name)
        return redirect("/add_list", code=302)

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=420,debug=True)