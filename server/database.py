import psycopg2
import os
from server import app


def test():
    db_url = app.config["DATABASE_URL"]
    
    conn = psycopg2.connect(db_url, sslmode="require")
    #conn = pg.DB(host="localhost", user="aslavin@nd.edu", passwd="Dameros123!", dbname="postgresql-graceful-05580")
    
    #query = "drop table FormEntries"
    query = """
    CREATE TABLE FormEntries (
                EntryID INTEGER NOT NULL,
                Message VARCHAR(255),
                PRIMARY KEY (EntryID)
                )
    """

    cursor = conn.cursor()
    cursor.execute(query)
    cursor.close()
    conn.commit()

    return "It worked"

