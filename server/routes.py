from server import app
from flask import render_template


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/apply')
def apply_func():
    return render_template("apply.html")
