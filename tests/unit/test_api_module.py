import sqlite3
from api_module import (get_currency_conversion_rate,
                        delete_users_and_accounts_with_missing_info, get_users_with_debts,
                        get_bank_with_highest_outbound_users,
                        get_bank_with_oldest_client, get_bank_with_largest_capital, get_user_transactions_last_3_months,
                        transfer_money, get_bank_name, assign_random_discounts)

from test_table_manipulation import (setup_database, create_users, create_banks,
                                     create_accounts, add_accounts, add_users)


def create_transaction():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Transact (Bank_sender_name, Account_sender_id, '
                   'Bank_receiver_name, Account_receiver_id, Sent_Currency, Sent_Amount, Datetime) '
                   'VALUES (?, ?, ?, ?, ?, ?, ?)', ('Bank1', 1, 'Bank2', 2, 'USD', 100, '2020-01-01'))
    conn.commit()
    conn.close()


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
