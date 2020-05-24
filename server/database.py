import psycopg2
from server import app

db_url = app.config["DATABASE_URL"]
conn = psycopg2.connect(db_url, sslmode="require")


"""
SQL injections
 - parameterizing queries (text inputs)
"""

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


def get_page_content(page_id):
    return get(f"SELECT * FROM dynamic_content WHERE page_id = {page_id}")


def update_element_content(element_id, content):
    push(f"UPDATE dynamic_content SET content = {content} WHERE element_id={element_id}")


def test():
    query = "INSERT INTO dynamic_content (element_id, page_id, content) VALUES ('#element2', 'home', 'test content2')"
    push(query)

    query = "SELECT * FROM dynamic_content WHERE page_id = 'home'"
    return get(query)


