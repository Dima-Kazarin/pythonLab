import sqlite3
import argparse


def create_tables(unique_by_fields=False):
    conn = sqlite3.connect('database.db')
    db_cursor = conn.cursor()

    db_cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Bank (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL UNIQUE
                    )
                ''')

    db_cursor.execute('''
                            CREATE TABLE IF NOT EXISTS Transact (
                                id INTEGER PRIMARY KEY,
                                Bank_sender_name TEXT NOT NULL,
                                Account_sender_id INTEGER NOT NULL,
                                Bank_receiver_name TEXT NOT NULL,
                                Account_receiver_id INTEGER NOT NULL,
                                Sent_Currency TEXT NOT NULL,
                                Sent_Amount REAL NOT NULL,
                                Datetime TEXT
                            )
                        ''')

    db_cursor.execute('''
                        CREATE TABLE IF NOT EXISTS User (
                            id INTEGER PRIMARY KEY,
                            Name TEXT NOT NULL ''' +
                      ('UNIQUE' if unique_by_fields else '') + ''',
                            Surname TEXT NOT NULL ''' +
                      ('UNIQUE' if unique_by_fields else '') + ''',
                            Birth_day TEXT,
                            Accounts TEXT NOT NULL
                        )
                ''')

    db_cursor.execute('''
                        CREATE TABLE IF NOT EXISTS Account (
                            id INTEGER PRIMARY KEY,
                            User_id INTEGER NOT NULL,
                            Type TEXT NOT NULL,
                            Account_Number TEXT NOT NULL UNIQUE,
                            Bank_id INTEGER NOT NULL,
                            Currency TEXT NOT NULL,
                            Amount REAL NOT NULL,
                            Status TEXT
                        )
                    ''')
    conn.commit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--unique', action='store_true',
                        help='Turn on uniqueness by fields Name and Surname.')
    args = parser.parse_args()

    create_tables(unique_by_fields=args.unique)
