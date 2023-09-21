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
    selectGuests = "Select name, group, 'u_group' From `guests`;"
    cursor = conn.execute(selectGuests)
    conn.commit()
    
    guests = []
    for c in cursor:
        guest = {
            'name':c[0],
            'group':c[1],
            'ugroup':c[2]
        }
        guests.append[guest]
    conn.close()
    return(guests)

@app.route("/home")
@app.route("/")
@app.route("/show_list")
def guests_list():
    guests = select_guests()
    return render_template("list.html")#, guests = guests)

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

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=420,debug=True)