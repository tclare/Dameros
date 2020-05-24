from server import app
from flask import render_template, jsonify, request
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


# start authentication
@app.route('/admin', methods=["GET", "POST"])
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


@app.route('/destroy_old_form_entries')
def destroy_old_form_entries():
    result = db_setup.drop_form_entries()
    return result


@app.route('/tilt_a_roll')
def tilt_a_roll_func():
    return render_template("play.html")


# authenticated
@app.route('/text_content', methods=['PUT'])
def text_content():
    ## TODO: Carefully check authentication (of Lauren) via session variables
    ### How to grab id and value that were just changed (error handle them): 
    id, value = request.json["id"], request.json["value"]
    ## TODO: Database update operation with these values that changes website content
    return jsonify({'success': 'yes'})


# authenticated
@app.route('/image_content', methods=['POST'])
def image_content():
    ## TODO: Carefully check authentication (of Lauren) via session variables
    ### How to grab image file that was just changed (error handle / make sure it has some content):
    #id   = dict(request.files).keys()[0]  ## ex. 'success-stories-image-1'. Id representing image file to change.
    id   = request.files["data"][0]
    #data = request.files[id]              ## ex. <FileStorage: 'fullsizeoutput_1f3.jpeg' ('image/jpeg')>. Contents of uploaded file.
    ## TODO: use github api ?? To upload this new file ??   https://developer.github.com/v3/repos/contents/#create-or-update-a-file ??
    ## TODO: git add, commit, push
    return jsonify({'success': 'yes', "data": str(id) })


@app.route('/create_db')
def create_db_func():
    db_setup.create_dynamic_content_table()
    db_setup.create_form_responses_table()


@app.route('/db_test')
def db_test_func():
    return str(database.test())


@app.route("/content/<page>")
def content(page):
    """TODO: process to key value pairs"""
    return jsonify(database.get_page_content(page))


"""
{
    status: success / error
    result:
         [
            { key : value },
            { key : value }
         ]

}
"""