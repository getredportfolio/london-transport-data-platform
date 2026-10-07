import os

import psycopg
from dotenv import load_dotenv

load_dotenv()



def get_connection():
    postgres_host = os.getenv("POSTGRES_HOST")
    postgres_port = int(os.getenv("POSTGRES_PORT", "5432"))
    postgres_db = os.getenv("POSTGRES_DB")
    postgres_user = os.getenv("POSTGRES_USER")
    postgres_password = os.getenv("POSTGRES_PASSWORD")

    connection = psycopg.connect(
        host=postgres_host,
        port=postgres_port,
        dbname=postgres_db,
        user=postgres_user,
        password=postgres_password,
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

