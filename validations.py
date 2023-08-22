import re
from datetime import datetime


def validate_user(data):
    """
    Validates the full name of a user.

    :param data: The full name to be validated.
    :return: A list containing two parts of the full name.
    """
    parts = data[0][0] if isinstance(data, list) else data[0]
    end = data[0][1:] if isinstance(data, list) else data[1:]

    name_parts = re.findall(r'\w+', parts)
    if len(name_parts) != 2:
        raise ValueError('Invalid user_full_name format')

    return [*parts.strip().split(), *end]


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


def validate_account_number(data):
    """
    Validates an account number with a specific format.

    :param data: The account number to be validated.
    :return: The validated account number.
    """
    account_number = data[2]
    account_number = re.sub(r'[#%_?&]', '-', account_number)
    if len(account_number) != 18:
        raise ValueError('Invalid account number length. It should be a string of 18 characters')

    if not re.match(r'ID--[a-zA-Z]{1,3}-\d+-', account_number):
        raise ValueError(
            'Invalid account number format. It should begin with "ID--", '
            'followed by 1 to 3 letters, a dash, '
            'one or more digits, and another dash')

    return data
