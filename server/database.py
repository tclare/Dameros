import psycopg2
import os
from server import app


def test():
    db_url = app.config["DATABASE_URL"]
    
    conn = psycopg2.connect(db_url, sslmode="require")

    query = "drop table Form Entries;"
#    query = """
#    CREATE TABLE FormEntries (
#                EntryID INTEGER NOT NULL,
#                Message VARCHAR(255),
#                PRIMARY KEY (EntryID)
#                )
#    """

    cursor = conn.cursor()
    cursor.execute(query)
    cursor.close()
    conn.commit()

    return "It worked"

