import psycopg2
from server import app
from functools import wraps


db_url = app.config["DATABASE_URL"]
conn = psycopg2.connect(db_url, sslmode="require")


"""
SQL injections
 - parameterizing queries (text inputs)
"""


class Pages:
    def __init__(self):
        self.content = dict()

    def register(self, page_name, all_records=False):
        """
        Decorator which fetches the page content from the database for
        a given `page_name`, then calls the route function

        ex:

        pages = Pages()

        @app.route("/")
        @pages.register("index")
        def index_func():
            ```
            page content for index.html has been injected into a dict of
            key-value pairs called "page_content"
            ```
            return render_template("index.html")
        """

        def decorator(endpoint_func):

            @wraps(endpoint_func)
            def wrapper(*endpoint_args, **endpoint_kwargs):
                self.content.clear()

                for row in get_page_content(page_name, all_records=all_records):
                    self.content[row[0]] = row[2]

                return endpoint_func(*endpoint_args, **endpoint_kwargs)

            return wrapper

        return decorator


def push(query, params=None):
    cursor = conn.cursor()

    if params:
        res = cursor.execute(query, params)
    else:
        res = cursor.execute(query)

    cursor.close()
    conn.commit()

    return res


def get(query, one=False, params=None):
    cursor = conn.cursor()

    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    if one:
        res = cursor.fetchone()
    else:
        res = cursor.fetchall()

    cursor.close()
    conn.commit()

    return res


def get_page_content(page_id, all_records=False):
    query = "SELECT * FROM dynamic_content WHERE page_id = %s OR %s"
    params = (page_id, all_records)
    return get(query, params=params)


def update_element_content(element_id, content):
    query = "UPDATE dynamic_content SET content = %s WHERE element_id=%s"
    params = (content, element_id)
    push(query, params=params)

    return "Success"


def insert_dynamic_content(element_id, page_id, content):
    query = "INSERT INTO dynamic_content (element_id, page_id, content) VALUES (%s, %s, %s)"
    params = (element_id, page_id, content)
    push(query, params=params)

    return "Success"

def insert_form_response(form_response):

    query = "INSERT INTO form_responses (name, email, sport, agent_email, agent_phone, time, interest) VALUES (%s, %s, %s, %s, %s, NOW(), %s)"
    # TODO: fix hard-coding by sending correct nfo from front end
    params = (form_response["name"], form_response["email"], form_response["sport"], "tclare@nd.edu", "012-345-6789", form_response["philanthropicInterest"])
    push(query, params=params)
    return "Success"

def get_form_responses(applicant_name='', all_records=False):

    query = "SELECT * FROM form_responses WHERE name = %s OR %s"
    params = (applicant_name, all_records)
    return get(query, params=params)

def insert_team_member(team_member):
    query = "INSERT INTO team_members (name, description) VALUES (%s, %s)"
    params = (team_member["name"], team_member["description"])
    push(query, params=params)
    return "Success"

def get_team_members():
    query = "SELECT * FROM team_members"
    return get(query)