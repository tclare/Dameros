import psycopg2
import os
from server import app


def test():
    url = app.config["DATABASE_URL"]
    conn = psycopg2.connect(url, sslmode="require")

    query = """
    CREATE TABLE FormEntries (
                EntryID INTEGER NOT NULL,
                Message VARCHAR(255),
                PRIMARY KEY (EntryID)
    """

    cursor = conn.cursor()
    cursor.execute(query)
    cursor.close()
    conn.commit()

    return "It worked"

