import random
from datetime import datetime, timedelta
import requests

from decorator import db_connection
from validations import validate_datetime
from table_manipulation import delete_user, delete_account

API = 'fca_live_OryVkPmOTHgVAjh3h5DhFFuUQc3QrUxLUAF7TPJA'
SELECT_BY_ID = 'SELECT {} FROM {} WHERE id = ?'
SELECT_FROM_TABLE = 'SELECT {} FROM {}'

UPDATE_ACCOUNT_BY_ID = 'UPDATE Account SET Amount = Amount {} ? WHERE id = ?'
DISCOUNTS = (25, 30, 50)


@db_connection
def get_bank_name(cursor, acc_id):
    """
    Get the name of the bank associated with an account.

    :param cursor: The database cursor object to execute SQL commands.
    :param acc_id: The account ID of the account to retrieve the associated bank name.
    :return: The name of the bank associated with the account.
    """
    cursor.execute(SELECT_BY_ID.format('Bank_id', 'Account'), (acc_id,))
    cursor.execute(SELECT_BY_ID.format('name', 'Bank'), (cursor.fetchone()[0],))
    return cursor.fetchone()[0]


def get_currency_conversion_rate(from_currency, to_currency):
    """
    Get the currency conversion rate from one currency to another using the Free Currency API.

    :param from_currency: The base currency code.
    :param to_currency: The target currency code for which the conversion rate is needed.
    :return: The currency conversion rate from `from_currency` to `to_currency`.
    """
    if from_currency == to_currency:
        return 1

    url = f'https://api.freecurrencyapi.com/v1/latest?apikey={API}' \
          f'&currencies={to_currency}&base_currency={from_currency}'
    data = requests.get(url, timeout=10).json()
    return data.get('data', {}).get(to_currency)


def get_currency_and_amount(cursor, acc_id):
    """
    Retrieve the currency and amount associated with the given account ID.

    :param cursor: A database cursor for executing SQL queries.
    :param acc_id: The ID of the account for which to fetch currency and amount.
    :return: A tuple containing the currency and amount (if available) associated with the account.
    """
    cursor.execute(SELECT_BY_ID.format('Currency, Amount', 'Account'), (acc_id,))
    return cursor.fetchone()


def check_availability(field, error_message):
    """
    Check the availability of a field and log an error message if it's not available.

    :param field: The field to be checked for availability.
    :param error_message: The error message to be logged if the field is not available.
    :return: The error message if the field is not available, otherwise None.
    """
    return error_message if not field else None


def conversion_accounts(cursor, sender_account_id, receiver_account_id, amount):
    """
    Perform currency conversion and update account balances for a transaction.

    :param cursor: A database cursor for executing SQL queries.
    :param sender_account_id: The ID of the sender's account.
    :param receiver_account_id: The ID of the receiver's account.
    :param amount: The amount to be transferred from sender to receiver.
    :return:
    A tuple containing sender's new balance, sender's currency, and amount in receiver's currency.
    """
    sender_account = get_currency_and_amount(cursor, sender_account_id)
    check_availability(sender_account, 'Sender account not found')
    receiver_account = get_currency_and_amount(cursor, receiver_account_id)
    check_availability(receiver_account, 'Receiver account not found')

    sender_currency, sender_balance = sender_account
    receiver_currency, _ = receiver_account

    conversion_rate = get_currency_conversion_rate(sender_currency, receiver_currency)
    check_availability(conversion_rate, 'Currency conversion rate not found')
    amount_in_receiver_currency = amount * conversion_rate

    return sender_balance, sender_currency, amount_in_receiver_currency


def perform_money_transfer(cursor, sender_balance, amount, sender_currency,
                           sender_account_id, amount_in_receiver_currency, receiver_account_id):
    if sender_balance >= amount:
        cursor.execute(UPDATE_ACCOUNT_BY_ID.format('-'),
                       (amount, sender_account_id))
        cursor.execute(UPDATE_ACCOUNT_BY_ID.format('+'),
                       (amount_in_receiver_currency, receiver_account_id))

        bank_sender_name = get_bank_name(sender_account_id)
        bank_receiver_name = get_bank_name(receiver_account_id)
        date_time = validate_datetime()
        cursor.execute('INSERT INTO Transact (Bank_sender_name, Account_sender_id, '
                       'Bank_receiver_name, Account_receiver_id, '
                       'Sent_Currency, Sent_Amount, Datetime) '
                       'VALUES(?, ?, ?, ?, ?, ?, ?)',
                       (bank_sender_name, sender_account_id, bank_receiver_name,
                        receiver_account_id, sender_currency, amount, date_time))

        return 'Money transferred successfully'

    return "Error: Sender's balance is not sufficient to perform the transaction"


@db_connection
def transfer_money(cursor, sender_account_id, receiver_account_id, amount):
    """
    Transfer money from the sender's account to the receiver's account.

    :param cursor: The database cursor object to execute SQL commands.
    :param sender_account_id: The ID of the sender's account.
    :param receiver_account_id: The ID of the receiver's account.
    :param amount:
    The amount to be transferred from the sender's account to the receiver's account.
    :return: A string indicating the result of the money transfer operation.
    """
    sender_balance, sender_currency, amount_in_receiver_currency = \
        conversion_accounts(cursor, sender_account_id, receiver_account_id, amount)

    perform_money_transfer(cursor, sender_balance, amount, sender_currency, sender_account_id,
                           amount_in_receiver_currency, receiver_account_id)


@db_connection
def assign_random_discounts(cursor):
    """
    Assign random discounts to a subset of users in the database.

    :param cursor: The database cursor object to execute SQL commands.
    :return: A dictionary containing user IDs as keys and randomly assigned discounts as values.
    """
    cursor.execute(SELECT_FROM_TABLE.format('id', 'User'))
    user_ids = [row[0] for row in cursor.fetchall()]
    num_users_to_choose = random.randint(1, min(10, len(user_ids)))
    chosen_user_ids = random.sample(user_ids, num_users_to_choose)
    user_ids_with_discounts = {user_id: random.choice(DISCOUNTS) for user_id in chosen_user_ids}

    return user_ids_with_discounts


@db_connection
def get_users_with_debts(cursor):
    """
    Retrieve the full names of users who have debts in their accounts.

    :param cursor: The database cursor object to execute SQL commands.
    :return: A list of full names of users with debts.
    """
    cursor.execute('SELECT User_id FROM Account WHERE Amount < 0')
    users_with_debts = cursor.fetchall()

    full_names = []
    for user_data in users_with_debts:
        user_id = user_data[0]
        cursor.execute(SELECT_BY_ID.format('Name, Surname', 'User'), (user_id,))
        user_name = cursor.fetchall()
        parse = [' '.join(name) for name in user_name]
        full_names.append(parse)

    return full_names


@db_connection
def get_bank_with_largest_capital(cursor):
    """
    Retrieve the bank name with the largest capital.

    :param cursor: The database cursor object to execute SQL commands.
    :return: A string indicating the bank that have the largest capital.
    """
    cursor.execute(SELECT_FROM_TABLE.format('Bank_id, Amount', 'Account'))
    acc = cursor.fetchall()
    banks = {bank_id: sum(user[1] for user in acc if user[0] == bank_id) for bank_id, _ in acc}

    b_id = max(banks, key=banks.get)
    cursor.execute(SELECT_BY_ID.format('name', 'Bank'), (b_id,))
    bank = cursor.fetchone()[0]
    return f'Bank which operates the biggest capital - {bank}'


@db_connection
def get_bank_with_oldest_client(cursor):
    """
    Retrieve the name of the bank that serves the oldest client.

    :param cursor: The database cursor object to execute SQL commands.
    :return: A string indicating the bank that serves the oldest client.
    """
    cursor.execute(SELECT_FROM_TABLE.format('Birth_day', 'User'))
    oldest_client_birth_day = min(birth_day[0] for birth_day in cursor.fetchall())

    cursor.execute('SELECT id FROM User WHERE Birth_day = ?', (oldest_client_birth_day,))
    user_id = cursor.fetchone()[0]
    bank_name = get_bank_name(user_id)
    return f'Bank which serves the oldest client - {bank_name}'


@db_connection
def get_bank_with_highest_outbound_users(cursor):
    """
    Retrieve bank with the highest outbound users.

    :param cursor: The database cursor object to execute SQL commands.
    :return: A string indicating the bank that have the highest outbound users.
    """
    cursor.execute(SELECT_FROM_TABLE.format('Bank_sender_name, Account_sender_id', 'Transact'))
    banks_users_count = {}

    for bank_name, account_id in cursor.fetchall():
        cursor.execute(SELECT_BY_ID.format('User_id', 'Account'), (account_id,))
        user_id = cursor.fetchone()

        banks_users_count.setdefault(bank_name, set())
        banks_users_count[bank_name].add(user_id)

    bank_with_highest_users = max(banks_users_count,
                                  key=lambda bank: len(banks_users_count[bank]))

    return f'Bank with the highest users which performed outbound transactions ' \
           f'- {bank_with_highest_users}'


def delete_users_or_accounts(cursor, table):
    if table == 'User':
        cursor.execute('SELECT id FROM User WHERE Name IS NULL OR Surname IS NULL '
                       'OR Birth_day IS NULL')
    else:
        cursor.execute('SELECT id FROM Account WHERE User_id IS NULL OR Type IS NULL '
                       'OR Account_Number IS NULL OR Bank_id IS NULL OR '
                       'Currency IS NULL OR Amount IS NULL OR Status IS NULL')
    return [row[0] for row in cursor.fetchall()]


@db_connection
def delete_users_and_accounts_with_missing_info(cursor):
    """
    Deletes users and accounts from the database if they have missing information.

    :param cursor: The database cursor object to execute SQL commands.
    :return: A message indicating the success of the operation.
    """
    users = delete_users_or_accounts(cursor, 'User')
    accounts = delete_users_or_accounts(cursor, 'Account')

    list(map(delete_user, users))
    list(map(delete_account, accounts))

    return 'Users and Accounts with missing information deleted successfully'


def parse_full_name(user_full_name):
    return user_full_name.strip().split()


@db_connection
def get_user_transactions_last_3_months(cursor, user_full_name):
    """
    Retrieve user transactions for last 3 months.

    :param cursor: The database cursor object to execute SQL commands.
    :param user_full_name: The full name of the user who have the transactions.
    :return: A list with user transactions.
    """
    name, surname = parse_full_name(user_full_name)
    cursor.execute('SELECT id FROM User WHERE Name = ? AND Surname = ?', (name, surname))
    (user_id,) = cursor.fetchone()
    check_availability(user_id, 'User not found')

    three_months = datetime.now() - timedelta(days=90)

    cursor.execute('SELECT * FROM Transact WHERE Account_sender_id = ? '
                   'OR Account_receiver_id = ? '
                   'AND DATETIME >= ?', (user_id, user_id, three_months))
    return cursor.fetchall()
