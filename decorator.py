import sqlite3


def db_connection(func):
    """
    Decorator for establishing a connection to an SQLite database.

    :param func: The function being decorated, expected to have the cursor as its first argument.
    :return: The wrapped function with a established database connection.
    """
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        result = func(cursor, *args, **kwargs)

        conn.commit()
        conn.close()

        return result

    return wrapper
