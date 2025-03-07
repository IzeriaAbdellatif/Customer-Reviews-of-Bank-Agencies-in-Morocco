import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "db1": {
        "dbname": os.getenv("POSTGRES_DB_1"),
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
        "host": os.getenv("POSTGRES_HOST"),
        "port": os.getenv("POSTGRES_PORT1"),
    },
    "db2": {
        "dbname": os.getenv("POSTGRES_DB_2"),
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
        "host": os.getenv("POSTGRES_HOST"),
        "port": os.getenv("POSTGRES_PORT2"),
    }
}
