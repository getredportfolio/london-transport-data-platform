import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT"))
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

def get_connection():
    connection = psycopg.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )
    return connection

def upsert_tube_lines(lines):
    connection = get_connection()
    cursor = connection.cursor()

    sql = """
    INSERT INTO tube_lines (line_id, line_name)
    VALUES (%s, %s)
    ON CONFLICT (line_id)
    DO UPDATE SET line_name = EXCLUDED.line_name;
    """
    for line in lines:
        cursor.execute(sql, (line.id, line.name))

    connection.commit()
    cursor.close()
    connection.close()

