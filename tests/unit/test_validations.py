from unittest.mock import patch

from validations import validate_datetime, validate_account_number, validate_strict_value, validate_user


def test_validate_user_full_name():
    data = ('John Do', '1990-01-01', 'acc1')
    actual = validate_user(data)
    assert actual == ['John', 'Do', '1990-01-01', 'acc1']


def test_validate_strict_value():
    field_name, value, allowed_values = 'gender', 'male', ['male', 'female']
    actual = validate_strict_value(field_name, value, allowed_values)
    assert actual is None


@patch('validations.datetime')
def test_validate_datetime(mock_f):
    datetime = '2023-08-05 12:30:00'
    actual = validate_datetime(datetime)
    assert actual == '2023-08-05 12:30:00'


def test_validate_account_number():
    data = (1, 'credit', 'ID--ss-1991111111-', 1, 'USD', 1000.0, 'gold')
    actual = validate_account_number(data)
    assert actual == (1, 'credit', 'ID--ss-1991111111-', 1, 'USD', 1000.0, 'gold')
