from server import app
from flask import render_template, jsonify
from server import database
from server import db_setup
import binascii


from flask import session, request, redirect, abort
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash


pages = database.Pages()


@app.context_processor
def page_content():
    # extend "page_content" as a global variable across all templates
    return dict(
        page_content=pages.content
    )


def login_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        password = session.get("password")
        goal     = app.config["ADMIN_PASSWORD"]

        if password and check_password_hash(password, goal):
            # passed authentication
            return func(*args, **kwargs)
        else:
            # must login first
            return redirect("/login")

    return decorator


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # hash password before assigning it to a session variable
        plain_text_password = request.form["password"]
        session["password"] = generate_password_hash(plain_text_password)

        return redirect("/admin")

    elif request.method == "GET":
        # load login form
        # 10 failed attempts per session
        session["attempts"] = session.get("attempts", 0) + 1

        if session["attempts"] > 10:
            return "Too many failed attempts"
        else:
            return render_template("login.html")

    # invalid method
    return abort(400)


@app.route('/')
@app.route('/index')
@pages.register("index")
def index():
    return render_template("index.html")


@app.route('/apply')
@pages.register("apply")
def apply_func():
    return render_template("apply.html")


@app.route('/success_stories')
@pages.register("success_stories")
def success_stories_func():
    return render_template("success_stories.html")


@app.route('/admin')
@pages.register("admin", all_records=True)
@login_required
def admin_func():
    return render_template("admin.html", authenticated=False)


@app.route('/tilt_a_roll')
def tilt_a_roll_func():
    return render_template("play.html")


@app.route('/text_content', methods=['PUT'])
@login_required
def text_content():
    # TODO: Carefully check authentication (of Lauren) via session variables
    # How to grab id and value that were just changed (error handle them):
    element_id, content = request.json["id"], request.json["value"]

    # database.update_element_content(element_id, content)

    return jsonify({'success': 'yes'})


@app.route('/image_content', methods=['POST'])
@login_required
def image_content():
    # TODO: Carefully check authentication (of Lauren) via session variables
    # How to grab image file that was just changed (error handle / make sure it has some content):
    # ex. 'success-stories-image-1'. Id representing image file to change.
    id = list(dict(request.files).keys())[0]
    binary_image_data = request.files[id].read()

    # ex. <FileStorage: 'fullsizeoutput_1f3.jpeg' ('image/jpeg')>. Contents of uploaded file.
    base_64_image_data = binascii.b2a_base64(binary_image_data)

    # TODO: use github api ?? To upload this new file ??
    # https://developer.github.com/v3/repos/contents/#create-or-update-a-file ??
    # The GitHub API only accepts base-64 encoding for file content, so that's the reason for base_64_image_data.
    # TODO: git add, commit, push

    return jsonify({'success': 'yes'})


@app.route('/apply_response', methods=['POST'])
def apply_response_func():
    form_response = request.json # ex. {'name': 'a', 'email': 'b', 'sport': 'c', 'donationAmount': '$0-$1,000', 'philanthropicInterest': 'd'}
    # TODO: insert data from response into db.
    return jsonify({'success': 'yes'})


@app.route('/test')
def test_func():
    return database.test()


@app.route("/demo")
@pages.register("demo")
def demo_func():
    return render_template("page_content_demo.html")
