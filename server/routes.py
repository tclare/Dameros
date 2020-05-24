from server import app
from flask import render_template
from server import database
from server import db_setup


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

@app.route('/admin')
def admin_func():
    return render_template("admin.html")

@app.route('/destroy_old_form_entries')
def destroy_old_form_entries():
    result = db_setup.drop_form_entries()
    return result

@app.route('/tilt_a_roll')
def tilt_a_roll_func():
    return render_template("play.html")

@app.route('/test')
def test_func():
    return database.test()