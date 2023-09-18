from flask import Flask, render_template, request, redirect
import dabase

app = Flask(__name__)

@app.route("/home")
@app.route("/")
def main():
    return render_template("index.html")

@app.route("/add_guest")
def add_guests():
    return render_template("index.html")

@app.route("/add_guest, methods =  ['POST', 'GET']")
def new_guest():
    if request.method == "POST":
        add_Guest
    return render_template("index.html")

@app.route("/show_list")
def guests_list():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host='127.0.0.1',port=420,debug=True)