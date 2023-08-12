import sqlite3
from unittest.mock import patch

from table_manipulation import (add_users, add_banks, add_accounts,
                                modify_user, modify_bank, modify_account, delete_user,
                                delete_bank, delete_account, parse_user_full_name)


def setup_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS User")
    cursor.execute("DROP TABLE IF EXISTS Bank")
    cursor.execute("DROP TABLE IF EXISTS Transact")
    cursor.execute("DROP TABLE IF EXISTS Account")
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS User (
                        id INTEGER PRIMARY KEY,
                        Name TEXT NOT NULL,
                        Surname TEXT NOT NULL,
                        Birth_day TEXT,
                        Accounts TEXT NOT NULL
                    )
                ''')
    cursor.execute('''
                        CREATE TABLE IF NOT EXISTS Bank (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL UNIQUE
                        )
                    ''')
    cursor.execute('''
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
    cursor.execute('''
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
    conn.close()


def create_users():
    add_users(('John Do', '1990-01-01', 'acc1'))
    add_users(('Jane Do', '1989-01-01', 'acc2'))


def create_banks():
    add_banks(('Bank1'))
    add_banks(('Bank2'))


def create_accounts():
    add_accounts((1, 'credit', '123456789', 1, 'USD', 2500.0, 'gold'))
    add_accounts((2, 'credit', '123456879', 2, 'USD', 1000.0, 'gold'))


def test_parse_user_full_name():
    full_name = 'John aa'
    actual = parse_user_full_name(full_name)
    assert actual == ('John', 'aa')


@patch('api_module.parse_user_full_name')
def test_add_users(mock_f):
    setup_database()

    data = ('John Do', '1990-01-01', 'acc1')
    mock_f.return_value = ('John', 'Do')

    actual = add_users(data)

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User WHERE name=?", ('John',))
    user = cursor.fetchone()
    conn.close()

    assert actual == 'Users added successfully'
    assert user is not None
    assert user[1] == 'John'
    assert user[2] == 'Do'
    assert user[3] == '1990-01-01'
    assert user[4] == 'acc1'


def test_add_banks():
    setup_database()

    data = ('Bank')

    actual = add_banks(data)

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Bank WHERE name=?", ('Bank',))
    bank = cursor.fetchone()
    conn.close()

    assert actual == 'Banks added successfully'
    assert bank[1] == 'Bank'


def test_add_accounts():
    setup_database()

    data = (1, 'credit', '123456789', 1, 'USD', 1000.0, 'gold')

    actual = add_accounts(data)

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Account WHERE User_id = ?", (1,))
    account = cursor.fetchone()
    conn.close()

    assert actual == 'Accounts added successfully'
    assert account[1] == 1
    assert account[2] == 'credit'
    assert account[3] == '123456789'
    assert account[4] == 1
    assert account[5] == 'USD'
    assert account[6] == 1000.0
    assert account[7] == 'gold'


def test_modify_user():
    setup_database()

    create_users()

    id = 1
    field = 'name'
    mod_field = 'Jo'

    actual = modify_user(id, field, mod_field)

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User WHERE id = ?", (id,))
    user = cursor.fetchone()
    conn.close()

    assert actual == 'Data modified successfully'
    assert user[1] == 'Jo'
    assert user[2] == 'Do'


def test_modify_bank():
    setup_database()

    create_banks()

    id = 1
    field = 'name'
    mod_field = 'Bank_1'

    actual = modify_bank(id, field, mod_field)

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Bank WHERE id = ?", (id,))
    bank = cursor.fetchone()
    conn.close()

    assert actual == 'Data modified successfully'
    assert bank[1] == 'Bank_1'


def test_modify_account():
    setup_database()

    create_accounts()

    id = 1
    field = 'Type'
    mod_field = 'debit'

    actual = modify_account(id, field, mod_field)

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Account WHERE id = ?", (id,))
    account = cursor.fetchone()
    conn.close()

    assert actual == 'Data modified successfully'
    assert account[2] == 'debit'


def test_delete_user():
    setup_database()

    create_users()

    id = 1
    actual = delete_user(id)

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User WHERE id = ?", (id,))
    user = cursor.fetchone()
    conn.close()

    assert actual == 'Data deleted successfully'
    assert user is None


def test_delete_bank():
    setup_database()

    create_banks()

    id = 1
    actual = delete_bank(id)

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Bank WHERE id = ?", (id,))
    bank = cursor.fetchone()
    conn.close()

    assert actual == 'Data deleted successfully'
    assert bank is None


def test_delete_account():
    setup_database()

    create_accounts()

    id = 1
    actual = delete_account(id)

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Account WHERE id = ?", (id,))
    account = cursor.fetchone()
    conn.close()

    assert actual == 'Data deleted successfully'
    assert account is None
