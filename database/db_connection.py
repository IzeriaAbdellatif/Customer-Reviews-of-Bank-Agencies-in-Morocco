import psycopg2
from db_config import DB_CONFIG


def get_connection(db_key):
    config = DB_CONFIG.get(db_key)
    if not config:
        raise ValueError(f"Invalid database key: {db_key}")

    try:
        conn = psycopg2.connect(**config)
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to {db_key}: {e}")
        return None
