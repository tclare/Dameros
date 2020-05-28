import psycopg2
from server import app
from functools import wraps


db_url = app.config["DATABASE_URL"]
# conn = psycopg2.connect(db_url, sslmode="require")


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

                for res in get_page_content(page_name, all_records=all_records):
                    self.content[res[0]] = res[2]

                return endpoint_func(*endpoint_args, **endpoint_kwargs)

            return wrapper

        return decorator


def push(text):
    cursor = conn.cursor()
    res = cursor.execute(text)
    cursor.close()
    conn.commit()

    return res


def get(text, one=False):
    cursor = conn.cursor()

    cursor.execute(text)

    if one:
        res = cursor.fetchone()
    else:
        res = cursor.fetchall()

    cursor.close()
    conn.commit()

    return res


def get_page_content(page_id, all_records=False):
    records = [
        ("#picture", "home", "pic"),
        ("#paragraph1", "demo", "abcdefg"),
        ("#paragraph2", "demo", "1234"),
        ("#paragraph3", "success_stories", "abcd"),
        ("#paragraph4", "apply", "bedef")
    ]

    return [
        r for r in records if (r[1] == page_id) or all_records
    ]

    # return get(f"SELECT * FROM dynamic_content WHERE page_id = {page_id} OR {all_records}")


def update_element_content(element_id, content):
    push(f"UPDATE dynamic_content SET content = {content} WHERE element_id={element_id}")


def test():
    query = "INSERT INTO dynamic_content (element_id, page_id, content) VALUES ('#element2', 'home', 'test content2')"
    push(query)

    query = "SELECT * FROM dynamic_content WHERE page_id = 'home'"
    return get(query)
