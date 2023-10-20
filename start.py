from flask import Flask, render_template, request, redirect, url_for
import dabase
import sqlite3 as sql

app = Flask(__name__)
    
def add_group(name, color):
    conn = sql.connect("lista_gości.db")
    conn.execute(f"""Insert Into 'groups' ('name', 'color') VALUES ('{name}', '{color}')""")
    conn.commit()
    conn.close()
    
def add_element(name, group, ugroup):
    conn = sql.connect("lista_gości.db")
    addElement = f"INSERT INTO `guests`(`name`,'group','u_group') VALUES ('{name}','{group}','{ugroup}')"
    conn.execute(addElement)
    conn.commit()
    conn.close()
    
def select_group():
    conn = sql.connect("lista_gości.db")
    selectGroups = "Select id, name, color From `groups`"
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

def select_ugroup():
    conn = sql.connect("lista_gości.db")
    select_ugroups = "Select id, name From `guests` Where u_group = 0 "
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

def select_elements():
    conn = sql.connect("lista_gości.db")
    selectElements = "Select id, `name`, `group`, `u_group`, `active` From `guests` Order by `group` asc;"
    selectColors = "Select color From `groups`"
    cursor = conn.execute(selectElements)
    cursor2 = conn.execute(selectColors)
    conn.commit()
    
    colors = []
    for c in cursor2:
        colors.append(c[0])
    elements = []
    for g in cursor:
        element = {
            'id':g[0],
            'name':g[1],
            'group':g[2],
            'u_group':g[3],
            'status':g[4],
            'color':colors[g[2]-1]
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
    
def reactive_element(id):
    conn = sql.connect("lista_gości.db")
    dezactiveGroup = f"UPDATE `guests` SET active = TRUE WHERE `id` = {id}"
    conn.execute(dezactiveGroup)
    conn.commit()
    conn.close()
    
def del_group(id):
    conn = sql.connect("lista_gości.db")
    deleteGroup = f"DELETE FROM `groups` WHERE `id` = {id};"
    conn.execute(deleteGroup)
    conn.commit()
    conn.close()

def del_element(id):
    conn = sql.connect("lista_gości.db")
    deleteList = f"DELETE FROM `lists` WHERE `id` = {id};"
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
    
@app.route("/home")
@app.route("/")
@app.route("/show_list")
def show_list():
    elements = select_elements()
    return render_template("list.html", el = elements, count = len(elements))

@app.route("/new_element", methods = ['POST'])
def new_element():
    if request.method == "POST":
        name = request.form['ename']
        group = request.form['egroup']
        ugroup = request.form['eugroup']
        add_element(name, group, ugroup)
        return redirect("/add_element", code=302)
    else:
        return redirect("/add_element", code=302)
    
@app.route("/new_group", methods = ['POST'])
def new_group():
    if request.method == "POST":
        name = request.form['gname']
        color = request.form['gcolor']
        add_group(name, color)
    return redirect("/add_element", code=302)

@app.route("/add_element")
def add_elements():
    groups = select_group()
    ugroups = select_ugroup()
    return render_template("add_element.html", groups = groups, ugroups = ugroups)

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
        if stat == "1":
            disctive_element(id)
        else:
            del_element(id)
        return redirect("/", code=302)
    
@app.route("/reload_element", methods = ['POST'])
def reload_element():
    if request.method == "POST":
        id = request.form['eid']
        reactive_element(id)
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