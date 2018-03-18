from pobuilds import app
from flask import render_template, redirect, url_for

@app.route('/')
@app.route('/index')
def index():
    return render_template("home/home.html")
