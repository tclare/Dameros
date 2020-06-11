import psycopg2
import os
from server import app


def drop_dynamic_content():
    db_url = app.config["DATABASE_URL"]
    
    conn = psycopg2.connect(db_url, sslmode="require")

    query = "DROP TABLE dynamic_content"

    cursor = conn.cursor()
    cursor.execute(query)
    cursor.close()
    conn.commit()
    conn.close()

    return "It worked"


def drop_form_entries():
    db_url = app.config["DATABASE_URL"]
    
    conn = psycopg2.connect(db_url, sslmode="require")

    query = "DROP TABLE form_responses"

    cursor = conn.cursor()
    cursor.execute(query)
    cursor.close()
    conn.commit()
    conn.close()

    return "It worked"


def create_dynamic_content_table():
    db_url = app.config["DATABASE_URL"]
    
    conn = psycopg2.connect(db_url, sslmode="require")
    
    query = """
        CREATE TABLE dynamic_content(
            element_id VARCHAR PRIMARY KEY,
            page_id VARCHAR,
            content VARCHAR
        )
    """

    cursor = conn.cursor()
    cursor.execute(query)
    cursor.close()
    conn.commit()
    conn.close()

    return "It worked"


def create_form_responses_table():
    db_url = app.config["DATABASE_URL"]
    
    conn = psycopg2.connect(db_url, sslmode="require")

    query = """
            CREATE TABLE form_responses(
                id SERIAL PRIMARY KEY,
                name VARCHAR NOT NULL,
                email VARCHAR,
                sport VARCHAR,
                agent_email VARCHAR,
                agent_phone VARCHAR,
                time TIMESTAMP NOT NULL, 
                interest VARCHAR
            )
        """

    cursor = conn.cursor()
    cursor.execute(query)
    cursor.close()
    conn.commit()
    conn.close()

    return "It worked"

def create_team_members_table():
    db_url = app.config["DATABASE_URL"]
    
    conn = psycopg2.connect(db_url, sslmode="require")
    
    query = """
        CREATE TABLE team_members(
            id SERIAL PRIMARY KEY,
            name VARCHAR NOT NULL,
            description VARCHAR
        )
    """

    cursor = conn.cursor()
    cursor.execute(query)
    cursor.close()
    conn.commit()
    conn.close()

    return "It worked"

def drop_team_members():
    db_url = app.config["DATABASE_URL"]
    
    conn = psycopg2.connect(db_url, sslmode="require")

    query = "DROP TABLE team_members"

    cursor = conn.cursor()
    cursor.execute(query)
    cursor.close()
    conn.commit()
    conn.close()

    return "It worked"