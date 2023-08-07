from validations import validate_datetime, validate_account_number, validate_strict_value, validate_user_full_name


def test_validate_user_full_name():
    name = 'John Do'
    actual = validate_user_full_name(name)
    assert actual == ['John', 'Do']


def test_validate_strict_value():
    field_name, value, allowed_values = 'gender', 'male', ['male', 'female']
    actual = validate_strict_value(field_name, value, allowed_values)
    assert actual is None


def test_validate_datetime():
    datetime = '2023-08-05 12:30:00'
    actual = validate_datetime(datetime)
    assert actual == '2023-08-05 12:30:00'


def test_validate_account_number():
    account_number = 'ID--st-1982721847-'
    actual = validate_account_number(account_number)
    assert actual == 'ID--st-1982721847-'
