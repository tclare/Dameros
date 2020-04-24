from server import app
from flask import render_template


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/apply')
def apply_func():
    return render_template("apply.html")

@app.route('/success_stories')
def success_stories_func():
    return render_template("success_stories.html")

@app.route('/tilt_a_roll')
def tilt_a_roll_func():
    return render_template("play.html")