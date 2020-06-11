from server import app
from flask import render_template, jsonify
from server import database
from server import db_setup
from PIL import Image
from io import BytesIO
import binascii
import github3

github_username = app.config["GITHUB_USERNAME"]
github_token = app.config["GITHUB_TOKEN"]
gh = github3.login(github_username, password=github_token)
repo = gh.repository("tclare", "Dameros")


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
        plain_text_password = request.json["password"]
        session["password"] = generate_password_hash(plain_text_password)

        # session will expire after 30 minutes
        session.permanent = True

        return jsonify({"success": "yes"})

    elif request.method == "GET":
        # load login form
        # 10 failed attempts per session
        session["attempts"] = session.get("attempts", 0) + 1

        # if session["attempts"] > 10:
        #     return "Too many failed attempts"
        # else:
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


@app.route('/update_text_content', methods=['PUT'])
@login_required
def update_text_content():
    # How to grab id and value that were just changed (error handle them):
    element_id, content = request.json["id"], request.json["value"]
    database.update_element_content(element_id, content)
    return jsonify({'success': 'yes'})


@app.route('/image_content', methods=['POST'])
@login_required
def image_content():
    ## TODO: Carefully check authentication (of Lauren) via session variables
    ### How to grab image file that was just changed (error handle / make sure it has some content):
    id = list(dict(request.files).keys())[0] ## ex. 'success-stories-image-1'. Id representing image file to change.
    binary_image_data = request.files[id].read() ## ex. <FileStorage: 'fullsizeoutput_1f3.jpeg' ('image/jpeg')>. Contents of uploaded file.
    
    # open image in pillow
    image = Image.open(BytesIO(binary_image_data))

    # continually decrease image size until it's less than 1MB
    size = 1000
    while True:
        image.thumbnail((size, size))
        output = BytesIO()
        image.save(output, format='PNG')
        if output.getbuffer().nbytes < 1000000:
            break
        size -= 200

    # push image to github
    hex_data = output.getvalue()
    update = repo.file_contents(f'/server/static/img/{id}.png').update(f'automatic update of image {id}', hex_data)

    return jsonify({'success': 'yes'})


@app.route('/apply_response', methods=['POST'])
def add_apply_response_func():
    form_response = request.json # ex. {'name': 'a', 'email': 'b', 'sport': 'c', 'donationAmount': '$0-$1,000', 'philanthropicInterest': 'd'}
    database.insert_form_response(form_response)
    return jsonify({'success': 'yes'})

# get application response -> specify person like /apply_response?name=Andy Slavin
@app.route('/apply_response', methods=['GET'])
@login_required
def get_apply_response_func():
    name = request.args.get('name')
    if name:
        response = database.get_form_responses(applicant_name=name)
    else:
        response = database.get_form_responses(all_records=True)
    return jsonify(response)


@app.route('/drop_databases')
@login_required
def drop_databases():
    x = db_setup.drop_team_members()
    x = db_setup.drop_form_entries()
    return db_setup.drop_dynamic_content()


@app.route('/create_databases')
@login_required
def create_databases():
    x = db_setup.create_team_members_table()
    x = db_setup.create_dynamic_content_table()
    return db_setup.create_form_responses_table()


@app.route('/add_everything')
@login_required
def add_everything():
    x = database.push('delete from dynamic_content where true')
    all_items = [
        ('index-text-1', 'index', 'Filler text: The University of Notre Dame du Lac (or simply Notre Dame /ˌnoʊtərˈdeɪm/ NOH-tər-DAYM, or ND) is a private Catholic research university in Notre Dame, Indiana, outside the city of South Bend.[7] It was founded in 1842 by Rev. Edward Sorin. The main campus covers 1,261 acres (510 ha) in a suburban setting; it contains a number of recognizable landmarks, such as the Golden Dome, the Word of Life mural (commonly known as Touchdown Jesus), Notre Dame Stadium, and the Basilica.'),
        ('index-text-2', 'index', 'Filler text: The University of Notre Dame du Lac (or simply Notre Dame /ˌnoʊtərˈdeɪm/ NOH-tər-DAYM, or ND) is a private Catholic research university in Notre Dame, Indiana, outside the city of South Bend.[7] It was founded in 1842 by Rev. Edward Sorin. The main campus covers 1,261 acres (510 ha) in a suburban setting; it contains a number of recognizable landmarks, such as the Golden Dome, the Word of Life mural (commonly known as Touchdown Jesus), Notre Dame Stadium, and the Basilica.'),
        ('success-stories-text-1', 'success_stories', '<h3>"A bird and a hand is worth two in the bush"</h3> <p class="carousel-text">-Neil Armstrong</p>'),
        ('success-stories-text-2', 'success_stories', '<h3>"Dameros is the best at what they do, hands down."</h3> <p class="carousel-text">-New York Times</p>'),
        ('success-stories-text-3', 'success_stories', '<h3>"Andy Slavin Sux"</h3> <p class="carousel-text">-Everyone</p>'),
        ('success-stories-text-4', 'success_stories', 'There are currently 31 undergraduate residence halls at the University of Notre Dame. Several of the halls are historic buildings which are listed on the National Register of Historic Places.[1] Each residence hall is single-sex, with 17 all-male residence halls and 14 all-female residence halls.[2] Notre Dame residence halls feature a mixed residential college and house system, where residence halls are the center of the student life and some academic teaching; most students stay at the same hall for most of their undergraduate studies.[3][4] Each hall has its own traditions, events, mascot, sports teams, shield, motto, and dorm pride.[5][6][7] The university also hosts Old College, an undergraduate residence for students preparing for the priesthood. Notre Dame has an undergraduate hall system which blends the residential college system and the house system. All first-year students are placed in one of the 31 halls upon enrollment, and students rarely switch halls. Each hall has its own spirit, tradition, mascot, sport teams, events, dances and reputation. Approximately 80% of undergraduate students live on campus, and often a student lives in the same dorm for the entirety of their undergraduate career.[8] A huge segment of student life happens through residence halls and students develop a particular attachment to their undergraduate hall. Each residence hall is directed by one Rector with the assistance of two Assistant Rectors and a variable number of Resident Assistants (from 4 to 9). Every residence hall has a chapel where Mass is held multiple time per week, fields a variety of intramural sports teams, elects one senator to represent the dorm in Student Government, and elects a president and vice president(s) which work through the Hall Presidents Council (HPC) student organization. Interhall football between Notre Dame male dorms is the only interhall tackle football which has remained at any US university.[9] Notre Dame residence halls are the center of the campus student life, and each one hosts signature events, like the Keenan Revue,[10] the Zahm Hall Bun run,[11] Fisher Regatta,[12] the Siegfried Day of Man, The Dillon Hall Pep Rally [13][14] and many others. Each dorm has its own architectural features, some of which were designed by famous architects such as Willoughby J. Edbrooke, Maginnis & Walsh and Thomas Ellerbe, and each hall has a chapel dedicated to the Hall''s patron saint.[15] With the exception of Carroll Hall, the residence halls are split among five main segments of the campus: Main (God) Quad, South Quad, North Quad, Mod Quad and West Quad. (Carroll has its own lawn, by Saint Mary\'s Lake, informally called "Far Quad.") All first-year students are not only guaranteed on-campus housing, but are required to reside on campus for at least six semesters, starting with the Class of 2022.[7] Many of the halls were inserted in 1973 on the National Register of Historic Places.'),
        ('success-stories-text-5', 'success_stories', 'There are currently 31 undergraduate residence halls at the University of Notre Dame. Several of the halls are historic buildings which are listed on the National Register of Historic Places.[1] Each residence hall is single-sex, with 17 all-male residence halls and 14 all-female residence halls.[2] Notre Dame residence halls feature a mixed residential college and house system, where residence halls are the center of the student life and some academic teaching; most students stay at the same hall for most of their undergraduate studies.[3][4] Each hall has its own traditions, events, mascot, sports teams, shield, motto, and dorm pride.[5][6][7] The university also hosts Old College, an undergraduate residence for students preparing for the priesthood. Notre Dame has an undergraduate hall system which blends the residential college system and the house system. All first-year students are placed in one of the 31 halls upon enrollment, and students rarely switch halls. Each hall has its own spirit, tradition, mascot, sport teams, events, dances and reputation. Approximately 80% of undergraduate students live on campus, and often a student lives in the same dorm for the entirety of their undergraduate career.[8] A huge segment of student life happens through residence halls and students develop a particular attachment to their undergraduate hall. Each residence hall is directed by one Rector with the assistance of two Assistant Rectors and a variable number of Resident Assistants (from 4 to 9). Every residence hall has a chapel where Mass is held multiple time per week, fields a variety of intramural sports teams, elects one senator to represent the dorm in Student Government, and elects a president and vice president(s) which work through the Hall Presidents Council (HPC) student organization. Interhall football between Notre Dame male dorms is the only interhall tackle football which has remained at any US university.[9] Notre Dame residence halls are the center of the campus student life, and each one hosts signature events, like the Keenan Revue,[10] the Zahm Hall Bun run,[11] Fisher Regatta,[12] the Siegfried Day of Man, The Dillon Hall Pep Rally [13][14] and many others. Each dorm has its own architectural features, some of which were designed by famous architects such as Willoughby J. Edbrooke, Maginnis & Walsh and Thomas Ellerbe, and each hall has a chapel dedicated to the Hall\'s patron saint.[15] With the exception of Carroll Hall, the residence halls are split among five main segments of the campus: Main (God) Quad, South Quad, North Quad, Mod Quad and West Quad. (Carroll has its own lawn, by Saint Mary\'s Lake, informally called "Far Quad.") All first-year students are not only guaranteed on-campus housing, but are required to reside on campus for at least six semesters, starting with the Class of 2022.[7] Many of the halls were inserted in 1973 on the National Register of Historic Places.'),
        ('success-stories-text-6', 'success_stories', 'There are currently 31 undergraduate residence halls at the University of Notre Dame. Several of the halls are historic buildings which are listed on the National Register of Historic Places.[1] Each residence hall is single-sex, with 17 all-male residence halls and 14 all-female residence halls.[2] Notre Dame residence halls feature a mixed residential college and house system, where residence halls are the center of the student life and some academic teaching; most students stay at the same hall for most of their undergraduate studies.[3][4] Each hall has its own traditions, events, mascot, sports teams, shield, motto, and dorm pride.[5][6][7] The university also hosts Old College, an undergraduate residence for students preparing for the priesthood. Notre Dame has an undergraduate hall system which blends the residential college system and the house system. All first-year students are placed in one of the 31 halls upon enrollment, and students rarely switch halls. Each hall has its own spirit, tradition, mascot, sport teams, events, dances and reputation. Approximately 80% of undergraduate students live on campus, and often a student lives in the same dorm for the entirety of their undergraduate career.[8] A huge segment of student life happens through residence halls and students develop a particular attachment to their undergraduate hall. Each residence hall is directed by one Rector with the assistance of two Assistant Rectors and a variable number of Resident Assistants (from 4 to 9). Every residence hall has a chapel where Mass is held multiple time per week, fields a variety of intramural sports teams, elects one senator to represent the dorm in Student Government, and elects a president and vice president(s) which work through the Hall Presidents Council (HPC) student organization. Interhall football between Notre Dame male dorms is the only interhall tackle football which has remained at any US university.[9] Notre Dame residence halls are the center of the campus student life, and each one hosts signature events, like the Keenan Revue,[10] the Zahm Hall Bun run,[11] Fisher Regatta,[12] the Siegfried Day of Man, The Dillon Hall Pep Rally [13][14] and many others. Each dorm has its own architectural features, some of which were designed by famous architects such as Willoughby J. Edbrooke, Maginnis & Walsh and Thomas Ellerbe, and each hall has a chapel dedicated to the Hall\'s patron saint.[15] With the exception of Carroll Hall, the residence halls are split among five main segments of the campus: Main (God) Quad, South Quad, North Quad, Mod Quad and West Quad. (Carroll has its own lawn, by Saint Mary\'s Lake, informally called "Far Quad.") All first-year students are not only guaranteed on-campus housing, but are required to reside on campus for at least six semesters, starting with the Class of 2022.[7] Many of the halls were inserted in 1973 on the National Register of Historic Places.'),
        ('apply-text-1', 'apply', '<ol> <li> Enter all your information in the fields below  </li> <li> Wait for a Dameros representative to respond to your query </li> <li> Enjoy your gauranteed results </li> </ol>'),

    ]
    for item in all_items:
        x = database.insert_dynamic_content(*item)
    
    return "it worked"

@app.route('/get_all_dynamic_content')
@login_required
def get_all_dynamic_content():
    return str(database.get_page_content('', True))

@app.route('/team_members', methods=['POST'])
@login_required
def add_team_member_func():
    team_member = request.json # ex. {'name': 'Andy Slavin', 'description': 'Andy is from California and blah blah blah...'}
    database.insert_team_member(team_member)
    return jsonify({'success': 'yes'})

@app.route('/team_members', methods=['GET'])
def get_team_members_func():
    return jsonify(database.get_team_members())