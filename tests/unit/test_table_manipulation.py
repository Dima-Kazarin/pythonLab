from unittest.mock import patch, MagicMock

from table_manipulation import (add_users, add_banks, add_accounts,
                                modify_user, modify_bank, modify_account, delete_user,
                                delete_bank, delete_account)


@patch('validations.validate_user')
def test_add_users(mock_f):
    cursor = MagicMock()
    data = ('John Do', '1990-01-01', 'acc1')
    mock_f.return_value = ['John', 'aa', 1, 1]

    actual = add_users.__wrapped__(cursor, data)

    assert actual == 'Data added successfully'
    cursor.execute.assert_called_once_with('INSERT INTO User (Name, Surname, Birth_day, Accounts) VALUES (?,?,?,?)',
                                           ['John', 'Do', '1990-01-01', 'acc1'])


def test_add_banks():
    cursor = MagicMock()
    data = ('Bank',)

    actual = add_banks.__wrapped__(cursor, data)

    assert actual == 'Data added successfully'
    cursor.execute.assert_called_once_with('INSERT INTO Bank (name) VALUES (?)', ('Bank',))


@patch('validations.validate_account_number')
def test_add_accounts(mock_f):
    cursor = MagicMock()

    data = (1, 'credit', 'ID--ss-1991111111-', 1, 'USD', 1000.0, 'gold')
    mock_f.return_value = (1, 'credit', 'ID--ss-1991111111-', 1, 'USD', 1000.0, 'gold')
    actual = add_accounts.__wrapped__(cursor, data)

    assert actual == 'Data added successfully'
    cursor.execute.assert_called_once_with('INSERT INTO Account '
                                           '(User_id, Type, Account_Number, Bank_id, Currency, Amount, Status) '
                                           'VALUES (?,?,?,?,?,?,?)',
                                           (1, 'credit', 'ID--ss-1991111111-', 1, 'USD', 1000.0, 'gold'))


def test_modify_user():
    cursor = MagicMock()

    id = 1
    field = 'name'
    mod_field = 'Jo'

    actual = modify_user.__wrapped__(cursor, id, field, mod_field)

    assert actual == 'Data modified successfully'
    cursor.execute.assert_called_once_with('UPDATE User SET name = ? WHERE id = ?', (mod_field, id))


def test_modify_bank():
    cursor = MagicMock()

    id = 1
    field = 'name'
    mod_field = 'Bank_1'

    actual = modify_bank.__wrapped__(cursor, id, field, mod_field)

    assert actual == 'Data modified successfully'
    cursor.execute.assert_called_once_with('UPDATE Bank SET name = ? WHERE id = ?', (mod_field, id))


def test_modify_account():
    cursor = MagicMock()

    id = 1
    field = 'Type'
    mod_field = 'debit'

    actual = modify_account.__wrapped__(cursor, id, field, mod_field)

    assert actual == 'Data modified successfully'
    cursor.execute.assert_called_once_with('UPDATE Account SET Type = ? WHERE id = ?', (mod_field, id))


def test_delete_user():
    cursor = MagicMock()

    id = 1
    actual = delete_user.__wrapped__(cursor, id)

    assert actual == 'Data deleted successfully'
    cursor.execute.assert_called_once_with('DELETE FROM User WHERE id = ?', (id,))


def test_delete_bank():
    cursor = MagicMock()

    id = 1
    actual = delete_bank.__wrapped__(cursor, id)

    assert actual == 'Data deleted successfully'
    cursor.execute.assert_called_once_with('DELETE FROM Bank WHERE id = ?', (id,))


def test_delete_account():
    cursor = MagicMock()

    id = 1
    actual = delete_account.__wrapped__(cursor, id)

    assert actual == 'Data deleted successfully'
    cursor.execute.assert_called_once_with('DELETE FROM Account WHERE id = ?', (id,))
