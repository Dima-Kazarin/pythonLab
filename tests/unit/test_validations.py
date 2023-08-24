from unittest.mock import patch
import pytest

from validations import validate_datetime, validate_account_number, validate_strict_value, validate_user


def test_validate_user_full_name():
    data = ('John Do', '1990-01-01', 'acc1')
    actual = validate_user(data)
    assert actual == ['John', 'Do', '1990-01-01', 'acc1']


def test_test_validate_user_full_name_error():
    data = ('John Do aa', '1990-01-01', 'acc1')
    with pytest.raises(ValueError):
        validate_user(data)


def test_validate_strict_value():
    field_name, value, allowed_values = 'gender', 'male', ['male', 'female']
    actual = validate_strict_value(field_name, value, allowed_values)
    assert actual is None


def test_validate_strict_value_error():
    field_name, value, allowed_values = 'gender', 'ma', ['male', 'female']
    with pytest.raises(ValueError):
        validate_strict_value(field_name, value, allowed_values)


@patch('validations.datetime')
def test_validate_datetime(mock_f):
    dt = '2023-08-05 12:30:00'
    actual = validate_datetime(dt)
    assert actual == dt


def test_validate_account_number():
    data = (1, 'credit', 'ID--1s3-ss-199-o-1', 1, 'USD', 1000.0, 'gold')
    actual = validate_account_number(data)
    assert actual == data


@pytest.mark.parametrize('data',
                         [
                             (1, 'credit', 'ID--1s3-ss-199-o-', 1, 'USD', 1000.0, 'gold'),
                             (1, 'credit', '12341s3-ss-199-o-1', 1, 'USD', 1000.0, 'gold'),
                             (1, 'credit', 'ID--1s3-ss-o-1', 1, 'USD', 1000.0, 'gold')
                         ])
def test_validate_account_number_error(data):
    with pytest.raises(ValueError):
        validate_account_number(data)
