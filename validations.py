import re
from datetime import datetime


def validate_user_full_name(name):
    """
    Validates the full name of a user.

    :param name: The full name to be validated.
    :return: A list containing two parts of the full name.
    """
    name_parts = re.findall(r'\w+', name)
    if len(name_parts) != 2:
        raise ValueError('Invalid user_full_name format')
    return name_parts


def validate_strict_value(field_name, value, allowed_values):
    """
    Validates if the given value is allowed for the specified field.

    :param field_name: The name of the field being validated.
    :param value: The value to be validated.
    :param allowed_values: The allowed values for the field.
    """
    if value not in allowed_values:
        raise ValueError(f'Not allowed value {value!r} for field "{field_name}"!')


def validate_datetime(dt=None):
    """
    Validates a datetime string or object.

    :param dt: The datetime string or object to be validated.
    :return: The validated datetime string in the format '%Y-%m-%d %H:%M:%S'.
    """
    if dt is None:
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return dt


def validate_account_number(account_number):
    """
    Validates an account number with a specific format.

    :param account_number: The account number to be validated.
    :return: The validated account number.
    """
    account_number = re.sub(r'[#%_?&]', '-', account_number)
    if len(account_number) != 18:
        raise ValueError('Invalid account number length. It should be a string of 18 characters')

    if not re.match(r'ID--[a-zA-Z]{1,3}-\d+-', account_number):
        raise ValueError(
            'Invalid account number format. It should begin with "ID--", '
            'followed by 1 to 3 letters, a dash, '
            'one or more digits, and another dash')

    return account_number
