from db_connection import get_connection


def insert_data(db_key, table_name, data):
    """
    Insert data into the specified table.

    :param db_key: Database key from db_config (e.g., "db1" or "db2").
    :param table_name: Table where data will be inserted.
    :param data: Dictionary containing column names as keys and values to insert.
    """
    conn = get_connection(db_key)
    if not conn:
        return

    cursor = conn.cursor()

    # Dynamically construct query
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    try:
        cursor.execute(query, tuple(data.values()))
        conn.commit()
        print(f"Data inserted into {table_name} of {db_key} successfully!")
    except Exception as e:
        print(f"Error inserting data: {e}")
        conn.rollback()

    cursor.close()
    conn.close()
