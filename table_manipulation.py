from csv import reader

from decorator import db_connection
from validations import validate_account_number, validate_user


def add_data_base(cursor, *args, validate_fnc=None, table, cols):
    data = args[0] if isinstance(args[0], list) else args
    for user_data in data:
        user_data = validate_fnc(user_data) if validate_fnc else user_data
        placeholders = ','.join(['?'] * len(user_data))
        cursor.execute(f'INSERT INTO {table} {cols} VALUES ({placeholders})', user_data)

    return 'Data added successfully'


@db_connection
def add_users(cursor, *args):
    """
    Add users to the 'User' table in the database.

    :param cursor: cursor object to execute SQL commands.
    :param args: Any number of user data tuples or a list of user data tuples.
    :return: A success message if users are added successfully.
    """
    return add_data_base(cursor, *args, validate_fnc=validate_user,
                         table='User', cols='(Name, Surname, Birth_day, Accounts)')


@db_connection
def add_banks(cursor, *args):
    """
    Add banks to the 'Bank' table in the database.

    :param cursor: cursor object to execute SQL commands.
    :param args: Any number of bank data tuples or a list of bank data tuples.
    :return: A success message if banks are added successfully.
    """
    return add_data_base(cursor, *args, table='Bank', cols='(name)')


@db_connection
def add_accounts(cursor, *args):
    """
    Add accounts to the 'Account' table in the database.

    :param cursor: cursor object to execute SQL commands.
    :param args: Any number of account data tuples or a list of account data tuples.
    :return: A success message if accounts are added successfully.
    """
    return add_data_base(cursor, *args, validate_fnc=validate_account_number, table='Account',
                         cols='(User_id, Type, Account_Number, Bank_id, Currency, Amount, Status)')


def read_csv_file(file_path, fnc):
    """
    Read data from a CSV file.

    :param fnc:
    :param file_path: The path of the CSV file to read.
    :return: A list of dictionaries representing the data from the CSV file.
    """
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        return fnc(list(reader(csvfile)))


def modify_base(cursor, user_id, field, mod_field, table):
    cursor.execute(f'UPDATE {table} SET {field} = ? WHERE id = ?', (mod_field, user_id))
    return 'Data modified successfully'


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
    return modify_base(cursor, user_id, field, mod_field, 'User')


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
    return modify_base(cursor, bank_id, field, mod_field, 'Bank')


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
    return modify_base(cursor, account_id, field, mod_field, 'Account')


def delete_base(cursor, user_id, table):
    cursor.execute(f'DELETE FROM {table} WHERE id = ?', (user_id,))
    return 'Data deleted successfully'


@db_connection
def delete_user(cursor, user_id):
    """
    Delete a user from the 'User' table.

    :param cursor: The database cursor object to execute SQL commands.
    :param user_id: The user ID of the user to be deleted.
    :return: A success message if the user is deleted successfully.
    """
    return delete_base(cursor, user_id, 'User')


@db_connection
def delete_bank(cursor, bank_id):
    """
    Delete a bank from the 'Bank' table.

    :param cursor: The database cursor object to execute SQL commands.
    :param bank_id: The bank ID of the bank to be deleted.
    :return: A success message if the bank is deleted successfully.
    """
    return delete_base(cursor, bank_id, 'Bank')


@db_connection
def delete_account(cursor, account_id):
    """
    Delete an account from the 'Account' table.

    :param cursor: The database cursor object to execute SQL commands.
    :param account_id: The account ID of the account to be deleted.
    :return: A success message if the account is deleted successfully.
    """
    return delete_base(cursor, account_id, 'Account')
