from server import app
from flask import render_template, jsonify, request
from server import database
from server import db_setup
import binascii


pages = database.Pages()


@app.context_processor
def page_content():
    # extend "page_content" as a global variable across all templates
    return dict(
        page_content=pages.content
    )


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
def admin_func():
    """
    if method == "GET" and session["authenticated"]:
        return render_template("admin.html")

    else:
        # database.get(password)
        # compare to request.form["password"]

        # good -> set session var
        session["authenticated"] = "yes"

        # bad -> return error
    """
    return render_template("admin.html")


@app.route('/tilt_a_roll')
def tilt_a_roll_func():
    return render_template("play.html")


# @authenticated
@app.route('/text_content', methods=['PUT'])
def text_content():
    # TODO: Carefully check authentication (of Lauren) via session variables
    # How to grab id and value that were just changed (error handle them):
    element_id, content = request.json["id"], request.json["value"]

    # database.update_element_content(element_id, content)

    return jsonify({'success': 'yes'})


# @authenticated
@app.route('/image_content', methods=['POST'])
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
@pages.register("demo", all_records=True)
def demo_func():
    return render_template("demo.html")
