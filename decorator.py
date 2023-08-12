import sqlite3

from logger import get_logger

logger = get_logger()


def db_connection(func):
    """
    Decorator for establishing a connection to an SQLite database.

    :param func: The function being decorated, expected to have the cursor as its first argument.
    :return: The wrapped function with established database connection.
    """

    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        try:
            result = func(cursor, *args, **kwargs)
            logger.info(result)
        except sqlite3.Error as e:
            logger.error(e)
            return f'Error: {e}'

        conn.commit()
        conn.close()

        return result

    return wrapper
