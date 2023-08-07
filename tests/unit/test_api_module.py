from unittest.mock import patch
import sqlite3
from api_module import (add_users, add_banks, add_accounts, modify_user, modify_bank, modify_account, delete_user,
                        delete_bank, delete_account, parse_user_full_name, get_currency_conversion_rate,
                        delete_users_and_accounts_with_missing_info, get_users_with_debts,
                        get_bank_with_highest_outbound_users,
                        get_bank_with_oldest_client, get_bank_with_largest_capital, get_user_transactions_last_3_months,
                        transfer_money,
                        get_bank_name, assign_random_discounts)


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


def create_transaction():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Transact (Bank_sender_name, Account_sender_id, '
                   'Bank_receiver_name, Account_receiver_id, Sent_Currency, Sent_Amount, Datetime) '
                   'VALUES (?, ?, ?, ?, ?, ?, ?)', ('Bank1', 1, 'Bank2', 2, 'USD', 100, '2020-01-01'))
    conn.commit()
    conn.close()


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

    assert actual == 'User data modified successfully'
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

    assert actual == 'Bank data modified successfully'
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

    assert actual == 'Account data modified successfully'
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

    assert actual == 'User deleted successfully'
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

    assert actual == 'Bank deleted successfully'
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

    assert actual == 'Account deleted successfully'
    assert account is None


def test_get_bank_name():
    setup_database()

    create_accounts()
    create_banks()

    acc_id = 1
    actual = get_bank_name(acc_id)

    assert actual == 'Bank1'


def test_get_currency_conversion_rate():
    from_cur = 'USD'
    to_cur = 'EUR'

    actual = get_currency_conversion_rate(from_cur, to_cur)

    assert 0.9 < actual < 1


def test_transfer_money():
    setup_database()

    create_accounts()
    create_banks()

    sender_acc_id = 1
    receiver_account_id = 2
    amount = 200

    actual = transfer_money(sender_acc_id, receiver_account_id, amount)

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT Amount FROM Account')
    account = cursor.fetchall()
    conn.close()

    assert actual == 'Money transferred successfully'
    assert account[0] == (2300.0,)
    assert account[1] == (1200.0,)


def test_assign_random_discounts():
    actual = assign_random_discounts()
    valid_discounts = [25, 30, 50]

    for discount in actual.values():
        assert discount in valid_discounts
    assert len(actual) <= 10


def test_get_users_with_debts():
    setup_database()

    add_accounts((1, 'credit', '123456789', 1, 'USD', -1000.0, 'gold'))
    create_users()

    actual = get_users_with_debts()

    assert actual == ['John Do']


def test_bank_with_largest_capital():
    setup_database()

    create_accounts()
    create_banks()

    actual = get_bank_with_largest_capital()
    assert actual == 'Bank which operates the biggest capital - Bank1'


def test_get_bank_with_oldest_client():
    setup_database()

    create_users()
    create_accounts()
    create_banks()

    actual = get_bank_with_oldest_client()

    assert actual == 'Bank which serves the oldest client - Bank2'


def test_get_bank_with_highest_outbound_users():
    setup_database()

    create_users()
    create_accounts()
    create_banks()
    create_transaction()

    actual = get_bank_with_highest_outbound_users()

    assert actual == 'Bank with the highest users which performed outbound transactions - Bank1'


def test_delete_users_and_accounts_with_missing_info():
    setup_database()

    add_users(('John Do', None, 'acc1'))
    add_accounts((1, 'credit', '123456789', 1, 'USD', 2500.0, None))

    actual = delete_users_and_accounts_with_missing_info()

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM User WHERE id = 1')
    user = cursor.fetchone()

    cursor.execute('SELECT * FROM Account WHERE id = 1')
    account = cursor.fetchone()
    conn.close()

    assert actual == 'Users and Accounts with missing information deleted successfully'
    assert user is None
    assert account is None


def test_get_user_transactions_last_3_months():
    setup_database()

    create_users()
    create_transaction()

    actual = get_user_transactions_last_3_months('John Do')

    assert actual == [(1, 'Bank1', 1, 'Bank2', 2, 'USD', 100.0, '2020-01-01')]
