import sqlite3
import csv
import random
from datetime import datetime, timedelta
import logging
import requests

from decorator import db_connection
from validations import validate_datetime

API = 'fca_live_OryVkPmOTHgVAjh3h5DhFFuUQc3QrUxLUAF7TPJA'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('logs.log')
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def parse_user_full_name(full_name):
    """
    Parse a full name into first name and surname.

    :param full_name:The full name to be parsed.
    :return:The first name and surname.
    """
    name, surname = full_name.strip().split(maxsplit=1)
    return name, surname


@db_connection
def add_users(cursor, *args):
    """
    Add users to the 'User' table in the database.

    :param cursor: cursor object to execute SQL commands.
    :param args: Any number of user data tuples or a list of user data tuples.
    :return: A success message if users are added successfully.
    """
    try:
        for users_data in args:
            if isinstance(users_data, list):
                for user_data in users_data:
                    full_name, birth_day, accounts = user_data
                    name, surname = parse_user_full_name(full_name)
                    cursor.execute('INSERT INTO User (Name, Surname, Birth_day, Accounts) '
                                   'VALUES (?, ?, ?, ?)',
                                   (name, surname, birth_day, accounts))
            else:
                full_name, birth_day, accounts = users_data
                name, surname = parse_user_full_name(full_name)
                cursor.execute('INSERT INTO User (Name, Surname, Birth_day, Accounts) '
                               'VALUES (?, ?, ?, ?)',
                               (name, surname, birth_day, accounts))

            logger.info('Users added successfully')
            return 'Users added successfully'
    except sqlite3.Error as e:
        logger.error('Unable to add users', e)
        return 'Unable to add users', e


@db_connection
def add_banks(cursor, *args):
    """
    Add banks to the 'Bank' table in the database.

    :param cursor: cursor object to execute SQL commands.
    :param args: Any number of bank data tuples or a list of bank data tuples.
    :return: A success message if banks are added successfully.
    """
    try:
        for banks_data in args:
            if isinstance(banks_data, list):
                for bank_data in banks_data:
                    cursor.execute('INSERT INTO Bank (name) VALUES (?)', (bank_data,))
            else:
                cursor.execute('INSERT INTO Bank (name) VALUES (?)', (banks_data,))
        logger.info('Banks added successfully')
        return 'Banks added successfully'
    except sqlite3.Error as e:
        logger.error('Unable to add banks', e)
        return 'Unable to add banks', e


@db_connection
def add_accounts(cursor, *args):
    """
    Add accounts to the 'Account' table in the database.

    :param cursor: cursor object to execute SQL commands.
    :param args: Any number of account data tuples or a list of account data tuples.
    :return: A success message if accounts are added successfully.
    """
    try:
        for accounts_data in args:
            if isinstance(accounts_data, list):
                for account_data in accounts_data:
                    user_id, account_type, account_number, bank_id, \
                        currency, amount, status = account_data
                    cursor.execute('INSERT INTO Account '
                                   '(User_id, Type, Account_Number, Bank_id, '
                                   'Currency, Amount, Status)'
                                   'VALUES (?, ?, ?, ?, ?, ?, ?)',
                                   (user_id, account_type, account_number,
                                    bank_id, currency, amount, status))
            else:
                user_id, account_type, account_number, \
                    bank_id, currency, amount, status = accounts_data
                cursor.execute('INSERT INTO Account '
                               '(User_id, Type, Account_Number, Bank_id, '
                               'Currency, Amount, Status)'
                               'VALUES (?, ?, ?, ?, ?, ?, ?)',
                               (user_id, account_type, account_number,
                                bank_id, currency, amount, status))
        logger.info('Accounts added successfully')
        return 'Accounts added successfully'
    except sqlite3.Error as e:
        logger.error('Unable to add accounts', e)
        return 'Unable to add accounts', e


def read_csv_file(file_path):
    """
    Read data from a CSV file.

    :param file_path: The path of the CSV file to read.
    :return: A list of dictionaries representing the data from the CSV file.
    """
    data = []
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(tuple(row))
    return data


@db_connection
def modify_user(cursor, user_id, field, mod_field):
    """
    Modify a field of a user in the 'User' table.

    :param cursor: The database cursor object to execute SQL commands.
    :param user_id: The user ID of the user to modify.
    :param field: The name of the field to modify.
    :param mod_field: The new value to set for the specified field.
    :return: A success message if the user data is modified successfully.
    """
    try:
        cursor.execute(f'UPDATE User SET {field} = ? WHERE id = ?', (mod_field, user_id))
        logger.info('User data modified successfully')
        return 'User data modified successfully'
    except sqlite3.Error as e:
        logger.error('Unable to modify user data', e)
        return 'Unable to modify user data', e


@db_connection
def modify_bank(cursor, bank_id, field, mod_field):
    """
    Modify a field of a bank in the 'Bank' table.

    :param cursor: The database cursor object to execute SQL commands.
    :param bank_id: The bank ID of the bank to modify.
    :param field: The name of the field to modify.
    :param mod_field: The new value to set for the specified field.
    :return: A success message if the bank data is modified successfully.
    """
    try:
        cursor.execute(f'UPDATE Bank SET {field} = ? WHERE id = ?', (mod_field, bank_id))
        logger.info('Bank data modified successfully')
        return 'Bank data modified successfully'
    except sqlite3.Error as e:
        logger.error('Unable to modify bank data', e)
        return 'Unable to modify bank data', e


@db_connection
def modify_account(cursor, account_id, field, mod_field):
    """
    Modify a field of an account in the 'Account' table.

    :param cursor: The database cursor object to execute SQL commands.
    :param account_id: The account ID of the account to modify.
    :param field: The name of the field to modify.
    :param mod_field: The new value to set for the specified field.
    :return: A success message if the account data is modified successfully.
    """
    try:
        cursor.execute(f'UPDATE Account SET {field} = ? WHERE id = ?', (mod_field, account_id))
        logger.info('Account data modified successfully')
        return 'Account data modified successfully'
    except sqlite3.Error as e:
        logger.error('Unable to modify account data', e)
        return 'Unable to modify account data', e


@db_connection
def delete_user(cursor, user_id):
    """
    Delete a user from the 'User' table.

    :param cursor: The database cursor object to execute SQL commands.
    :param user_id: The user ID of the user to be deleted.
    :return: A success message if the user is deleted successfully.
    """
    try:
        cursor.execute('DELETE FROM User WHERE id = ?', (user_id,))
        logger.info('User deleted successfully')
        return 'User deleted successfully'
    except sqlite3.Error as e:
        logger.error('Unable to delete user', e)
        return 'Unable to delete user', e


@db_connection
def delete_bank(cursor, bank_id):
    """
    Delete a bank from the 'Bank' table.

    :param cursor: The database cursor object to execute SQL commands.
    :param bank_id: The bank ID of the bank to be deleted.
    :return: A success message if the bank is deleted successfully.
    """
    try:
        cursor.execute('DELETE FROM Bank WHERE id = ?', (bank_id,))
        logger.info('Bank deleted successfully')
        return 'Bank deleted successfully'
    except sqlite3.Error as e:
        logger.error('Unable to delete bank', e)
        return 'Unable to delete bank', e


@db_connection
def delete_account(cursor, account_id):
    """
    Delete an account from the 'Account' table.

    :param cursor: The database cursor object to execute SQL commands.
    :param account_id: The account ID of the account to be deleted.
    :return: A success message if the account is deleted successfully.
    """
    try:
        cursor.execute('DELETE FROM Account WHERE id = ?', (account_id,))
        logger.info('Account deleted successfully')
        return 'Account deleted successfully'
    except sqlite3.Error as e:
        logger.error('Unable to delete account', e)
        return 'Unable to delete account', e


@db_connection
def get_bank_name(cursor, acc_id):
    """
    Get the name of the bank associated with an account.

    :param cursor: The database cursor object to execute SQL commands.
    :param acc_id: The account ID of the account to retrieve the associated bank name.
    :return: The name of the bank associated with the account.
    """
    cursor.execute('SELECT Bank_id FROM Account WHERE id = ?', (acc_id,))
    bank_id = cursor.fetchone()[0]
    cursor.execute('SELECT name FROM Bank WHERE id = ?', (bank_id,))
    return cursor.fetchone()[0]


def get_currency_conversion_rate(from_currency, to_currency):
    """
    Get the currency conversion rate from one currency to another using the Free Currency API.

    :param from_currency: The base currency code.
    :param to_currency: The target currency code for which the conversion rate is needed.
    :return: The currency conversion rate from `from_currency` to `to_currency`.
    """
    url = f'https://api.freecurrencyapi.com/v1/latest?apikey={API}' \
          f'&currencies={to_currency}&base_currency={from_currency}'
    response = requests.get(url, timeout=10)
    data = response.json()

    return data.get('data', {}).get(to_currency)


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
    try:
        cursor.execute('SELECT Currency, Amount FROM Account WHERE id = ?', (sender_account_id,))
        sender_account = cursor.fetchone()
        if not sender_account:
            logger.error('Sender account not found')
            return 'Sender account not found'

        cursor.execute('SELECT Currency, Amount FROM Account WHERE id = ?', (receiver_account_id,))
        receiver_account = cursor.fetchone()
        if not receiver_account:
            logger.error('Receiver account not found')
            return 'Receiver account not found'

        sender_currency, sender_balance = sender_account
        receiver_currency, _ = receiver_account

        if sender_currency != receiver_currency:
            conversion_rate = get_currency_conversion_rate(sender_currency, receiver_currency)
            if not conversion_rate:
                logger.error('Currency conversion rate not found')
                return 'Currency conversion rate not found'

            amount_in_receiver_currency = amount * conversion_rate
        else:
            amount_in_receiver_currency = amount

        if sender_balance >= amount:
            cursor.execute('UPDATE Account SET Amount = Amount - ? WHERE id = ?',
                           (amount, sender_account_id))
            cursor.execute('UPDATE Account SET Amount = Amount + ? WHERE id = ?',
                           (amount_in_receiver_currency, receiver_account_id))

            bank_sender_name = get_bank_name(sender_account_id)
            bank_receiver_name = get_bank_name(receiver_account_id)
            date_time = validate_datetime(None)
            cursor.execute('INSERT INTO Transact (Bank_sender_name, Account_sender_id, '
                           'Bank_receiver_name, Account_receiver_id, '
                           'Sent_Currency, Sent_Amount, Datetime) '
                           'VALUES(?, ?, ?, ?, ?, ?, ?)',
                           (bank_sender_name, sender_account_id, bank_receiver_name,
                            receiver_account_id, sender_currency, amount, date_time))
            logger.info('Money transferred successfully')
            return 'Money transferred successfully'

        logger.error("Sender's balance is not sufficient to perform the transaction")
        return "Error: Sender's balance is not sufficient to perform the transaction"
    except sqlite3.Error as e:
        logger.error('Unable to perform money transfer', e)
        return 'Unable to perform money transfer', e


@db_connection
def assign_random_discounts(cursor):
    """
    Assign random discounts to a subset of users in the database.

    :param cursor: The database cursor object to execute SQL commands.
    :return: A dictionary containing user IDs as keys and randomly assigned discounts as values.
    """
    discounts = [25, 30, 50]

    try:
        cursor.execute('SELECT id FROM User')
        user_ids = [row[0] for row in cursor.fetchall()]
        num_users_to_choose = min(10, len(user_ids))
        chosen_user_ids = random.sample(user_ids, num_users_to_choose)
        user_discounts = {}
        for user_id in chosen_user_ids:
            discount = random.choice(discounts)
            user_discounts[user_id] = discount

        return user_discounts
    except sqlite3.Error as e:
        logger.error('Unable to assign random discounts', e)
        return 'Unable to assign random discounts', e


@db_connection
def get_users_with_debts(cursor):
    """
    Retrieve the full names of users who have debts in their accounts.

    :param cursor: The database cursor object to execute SQL commands.
    :return: A list of full names of users with debts.
    """
    try:
        cursor.execute('SELECT User_id FROM Account WHERE Amount < 0')
        users_with_debts = cursor.fetchall()
        full_names = []
        for user_data in users_with_debts:
            user_id = user_data[0]
            cursor.execute('SELECT Name, Surname FROM User WHERE id = ?', (user_id,))
            user_name = cursor.fetchall()
            for name in user_name:
                full_name = ' '.join(name)
            full_names.append(full_name)

        return full_names

    except sqlite3.Error as e:
        logger.error('Unable to get users with debts', e)
        return 'Unable to get users with debts', e


@db_connection
def get_bank_with_largest_capital(cursor):
    """
    Retrieve the bank name with the largest capital.

    :param cursor: The database cursor object to execute SQL commands.
    :return: A string indicating the bank that have the largest capital.
    """
    try:
        cursor.execute('SELECT Bank_id, Amount FROM Account')
        acc = cursor.fetchall()
        banks = {}
        for user in acc:
            bank_id = user[0]
            amount = user[1]
            banks[bank_id] = banks.get(bank_id, 0) + amount

        b_id = max(banks, key=banks.get)
        cursor.execute('SELECT name FROM Bank WHERE id = ?', (b_id,))
        bank = cursor.fetchone()[0]
        logger.info('Bank which operates the biggest capital - %s', bank)
        return f'Bank which operates the biggest capital - {bank}'
    except sqlite3.Error as e:
        logger.error('Unable to find bank with largest capital', e)
        return 'Unable to find bank with largest capital', e


@db_connection
def get_bank_with_oldest_client(cursor):
    """
    Retrieve the name of the bank that serves the oldest client.

    :param cursor: The database cursor object to execute SQL commands.
    :return: A string indicating the bank that serves the oldest client.
    """
    try:
        cursor.execute('SELECT Birth_day FROM User')
        birth_days = cursor.fetchall()
        birth_days = [birth_day[0] for birth_day in birth_days]
        oldest_client_birth_day = min(birth_days)

        cursor.execute('SELECT id FROM User WHERE Birth_day = ?', (oldest_client_birth_day,))
        user_id = cursor.fetchone()[0]
        bank_name = get_bank_name(user_id)
        logger.info('Bank which serves the oldest client - %s', bank_name)
        return f'Bank which serves the oldest client - {bank_name}'
    except sqlite3.Error as e:
        logger.error('Unable to find bank with oldest client', e)
        return 'Unable to find bank with oldest client', e


@db_connection
def get_bank_with_highest_outbound_users(cursor):
    """
    Retrieve bank with the highest outbound users.

    :param cursor: The database cursor object to execute SQL commands.
    :return: A string indicating the bank that have the highest outbound users.
    """
    try:
        cursor.execute('SELECT Bank_sender_name, Account_sender_id FROM Transact')
        banks_users_count = {}

        for bank_name, account_id in cursor.fetchall():
            cursor.execute('SELECT User_id FROM Account WHERE id = ?', (account_id,))
            user_id = cursor.fetchone()[0]

            banks_users_count[bank_name] = banks_users_count.get(bank_name, set())
            banks_users_count[bank_name].add(user_id)

        max_users_count = 0
        bank_with_highest_users = None

        for bank_name, users_set in banks_users_count.items():
            if len(users_set) > max_users_count:
                max_users_count = len(users_set)
                bank_with_highest_users = bank_name

        logger.info('Bank with the highest users which performed outbound transactions - %s',
                    bank_with_highest_users)
        return f'Bank with the highest users which performed outbound transactions ' \
               f'- {bank_with_highest_users}'
    except sqlite3.Error as e:
        logger.error('Unable to find bank with highest outbound users', e)
        return 'Unable to find bank with highest outbound users', e


@db_connection
def delete_users_and_accounts_with_missing_info(cursor):
    """
    Deletes users and accounts from the database if they have missing information.

    :param cursor: The database cursor object to execute SQL commands.
    :return: A message indicating the success of the operation.
    """
    try:
        cursor.execute('SELECT id FROM User WHERE Name IS NULL OR Surname IS NULL '
                       'OR Birth_day IS NULL')
        user_ids_with_missing_info = [row[0] for row in cursor.fetchall()]

        for user_id in user_ids_with_missing_info:
            delete_user(user_id)

        cursor.execute('SELECT id FROM Account WHERE User_id IS NULL OR Type IS NULL '
                       'OR Account_Number IS NULL OR Bank_id IS NULL OR '
                       'Currency IS NULL OR Amount IS NULL OR Status IS NULL ')
        account_ids_with_missing_info = [row[0] for row in cursor.fetchall()]

        for account_id in account_ids_with_missing_info:
            delete_account(account_id)

        logger.info('Users and Accounts with missing information deleted successfully')
        return 'Users and Accounts with missing information deleted successfully'
    except sqlite3.Error as e:
        logger.error('Unable to delete users with missing information', e)
        return 'Unable to delete users with missing information', e


@db_connection
def get_user_transactions_last_3_months(cursor, user_full_name):
    """
    Retrieve user transactions for last 3 months.

    :param cursor: The database cursor object to execute SQL commands.
    :param user_full_name: The full name of the user who have the transactions.
    :return: A list with user transactions.
    """
    try:
        name, surname = parse_user_full_name(user_full_name)
        cursor.execute('SELECT id FROM User WHERE Name = ? AND Surname = ?', (name, surname))
        user_id = cursor.fetchone()
        if not user_id:
            logger.error('User not found')
            return 'User not found'

        user_id = user_id[0]
        three_months = datetime.now() - timedelta(days=90)

        cursor.execute('SELECT * FROM Transact WHERE Account_sender_id = ? '
                       'OR Account_receiver_id = ? '
                       'AND DATETIME >= ?', (user_id, user_id, three_months))
        data = cursor.fetchall()
        logger.info(data)
        return data

    except sqlite3.Error as e:
        logger.error('Unable to fetch user transactions', e)
        return 'Unable to fetch user transactions', e
