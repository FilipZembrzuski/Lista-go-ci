from flask import Flask, render_template, request, redirect, url_for
import dabase
import sqlite3 as sql

app = Flask(__name__)
    
def add_group(name, color):
    conn = sql.connect("lista_gości.db")
    conn.execute(f"""Insert Into 'groups' ('name', 'color') VALUES ('{name}', '{color}')""")
    conn.commit()
    conn.close()
    
def add_guest(name, group, ugroup):
    conn = sql.connect("lista_gości.db")
    addGuest = f"INSERT INTO `guests`(`name`,'group','u_group') VALUES ('{name}','{group}','{ugroup}')"
    conn.execute(addGuest)
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

def select_guests():
    conn = sql.connect("lista_gości.db")
    selectGuests = "Select id, `name`, `group`, `u_group`, `active` From `guests` Order by `group` asc;"
    selectColors = "Select color From `groups`"
    cursor = conn.execute(selectGuests)
    cursor2 = conn.execute(selectColors)
    conn.commit()
    
    colors = []
    for c in cursor2:
        colors.append(c[0])
    guests = []
    for g in cursor:
        guest = {
            'id':g[0],
            'name':g[1],
            'group':g[2],
            'u_group':g[3],
            'status':g[4],
            'color':colors[g[2]-1]
        }
        guests.append(guest)
        
    conn.close()
    return(guests)

def disctive_guest(id):
    conn = sql.connect("lista_gości.db")
    dezactiveGroup = f"UPDATE `guests` SET active = FALSE WHERE `id` = {id}"
    conn.execute(dezactiveGroup)
    conn.commit()
    conn.close()
    
def reactive_guest(id):
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

def del_guest(id):
    conn = sql.connect("lista_gości.db")
    deleteGuest = f"DELETE FROM `guests` WHERE `id` = {id};"
    deleteUguest = f"DELETE FROM `guests` WHERE `u_group` = {id};"
    conn.execute(deleteGuest)
    conn.execute(deleteUguest)
    conn.commit()
    conn.close()

def edit_groups(id, color):
    conn = sql.connect("lista_gości.db")
    updateGroup = f"UPDATE `groups` SET color='{color}' WHERE `id` = {id}"
    conn.execute(updateGroup)
    conn.commit()
    conn.close()
    
@app.route("/home")
@app.route("/")
@app.route("/show_list")
def guests_list():
    guests = select_guests()
    return render_template("list.html", guests = guests, count = len(guests))

@app.route("/new_guest", methods = ['POST'])
def new_guest():
    if request.method == "POST":
        name = request.form['pname']
        group = request.form['pgroup']
        ugroup = request.form['pugroup']
        add_guest(name, group, ugroup)
        return redirect("/add_guest", code=302)
    else:
        return redirect("/add_guest", code=302)
    
@app.route("/new_group", methods = ['POST'])
def new_group():
    if request.method == "POST":
        name = request.form['gname']
        color = request.form['gcolor']
        add_group(name, color)
    return redirect("/add_guest", code=302)

@app.route("/add_guest")
def add_guests():
    groups = select_group()
    ugroups = select_ugroup()
    return render_template("add_guest.html", groups = groups, ugroups = ugroups)

@app.route("/delete_group", methods = ['POST'])
def delete_group():
    if request.method == "POST":
        id = request.form['gid']
        del_group(id)
        return redirect("/add_guest", code=302)
    
@app.route("/delete_guest", methods = ['POST'])
def delete_guest():
    if request.method == "POST":
        id = request.form['gid']
        stat = request.form['stat']
        if stat == "1":
            disctive_guest(id)
        else:
            del_guest(id)
        return redirect("/", code=302)
    
@app.route("/reload_guest", methods = ['POST'])
def reload_guest():
    if request.method == "POST":
        id = request.form['gid']
        reactive_guest(id)
        return redirect("/", code=302)
    
@app.route("/edit_group", methods = ['POST'])
def update_group():
    if request.method == "POST":
        id = request.form['gid']
        color = request.form['ucolor']
        edit_groups(id, color)
        return redirect("/add_guest", code=302)
    

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=420,debug=True)