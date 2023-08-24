from unittest.mock import MagicMock, patch, call
import pytest

from api_module import (get_users_with_debts, assign_random_discounts, get_bank_with_highest_outbound_users,
                        conversion_accounts, get_currency_and_amount, get_bank_name,
                        get_bank_with_largest_capital, get_bank_with_oldest_client,
                        get_user_transactions_last_3_months, delete_users_or_accounts,
                        delete_users_and_accounts_with_missing_info, get_currency_conversion_rate,
                        transfer_money, check_availability)

BANK = 'Bank'


def test_get_bank_name(cursor):
    cursor.fetchone.return_value = (BANK,)
    actual = get_bank_name.__wrapped__(cursor, None)

    assert actual == BANK


@patch('api_module.requests.get')
def test_get_currency_conversion_rate(mock_f):
    from_cur = 'USD'
    to_cur = 'EUR'
    mock_json = MagicMock(return_value={'data': {'EUR': 0.91}})
    mock_f.return_value.json = mock_json

    actual = get_currency_conversion_rate(from_cur, to_cur)

    assert actual == 0.91


def test_get_currency_and_amount(cursor):
    id = 1
    get_currency_and_amount(cursor, id)

    cursor.execute.assert_called_once_with('SELECT Currency, Amount FROM Account WHERE id = ?', (id,))


@pytest.mark.parametrize('field, error_message, expected',
                         [
                             (None, 'Error', 'Error'),
                             (1, 'Error', None)
                         ])
def test_check_availability(field, error_message, expected):
    actual = check_availability(field, error_message)

    assert actual == expected


@patch('api_module.get_currency_conversion_rate')
@patch('api_module.get_currency_and_amount')
@patch('api_module.check_availability')
def test_conversion_accounts(mock_f, mock_c, mock_a, cursor):
    mock_c.return_value = ('USD', 900)
    mock_f.return_value = None
    mock_a.return_value = 1

    actual = conversion_accounts(cursor, 1, 2, 100)

    assert actual == (900, 'USD', 100)


@patch('api_module.conversion_accounts')
@patch('api_module.get_bank_name')
@patch('validations.validate_datetime')
def test_transfer_money(mock_dt, mock_bn, mock_f, cursor):
    sender_acc_id = 1
    receiver_account_id = 2
    amount = 200
    mock_dt.return_value = '2023-08-22 11:51:01'
    mock_bn.side_effect = ['Bank1', 'Bank2']

    cursor.execute.side_effect = [None, None, None]
    mock_f.return_value = 200, 'USD', 200
    transfer_money.__wrapped__(cursor, sender_acc_id, receiver_account_id, amount)

    cursor.execute.assert_has_calls([call('UPDATE Account SET Amount = Amount - ? WHERE id = ?',
                                          (amount, sender_acc_id)),
                                     call('UPDATE Account SET Amount = Amount + ? WHERE id = ?',
                                          (amount, receiver_account_id)), ])


@patch('api_module.random.randint')
@patch('api_module.random.sample')
@patch('api_module.random.choice')
def test_assign_random_discounts(mock_random_sample, mock_random_choice, mock_random_randint, cursor):
    user_ids = [1, 2, 3, 4, 5]
    chosen_user_ids = [1, 3]

    cursor.execute.return_value = user_ids
    mock_random_randint.return_value = 2
    mock_random_sample.side_effect = [25, 50]
    mock_random_choice.return_value = chosen_user_ids

    actual = assign_random_discounts.__wrapped__(cursor)

    assert actual == {1: 25, 3: 50}


def test_get_users_with_debts(cursor):
    cursor.fetchall.side_effect = [[(1,), (2,)], [('Jo', 'aa')], [('Jo2', 'aa')]]
    actual = get_users_with_debts.__wrapped__(cursor)

    assert actual == [['Jo aa'], ['Jo2 aa']]


def test_bank_with_largest_capital(cursor):
    cursor.fetchall.return_value = [(1, 100), (1, 1000), (2, 500)]
    cursor.fetchone.return_value = ('Bank1', 'Bank2')

    actual = get_bank_with_largest_capital.__wrapped__(cursor)
    assert actual == 'Bank which operates the biggest capital - Bank1'
    cursor.execute.assert_called_with('SELECT name FROM Bank WHERE id = ?', (1,))


@patch('api_module.get_bank_name')
def test_get_bank_with_oldest_client(mock_f, cursor):
    cursor.fetchall.return_value = [('1990-01-01',), ('2000-01-01',)]
    cursor.fetchone.return_value = (BANK,)
    mock_f.return_value = BANK

    actual = get_bank_with_oldest_client.__wrapped__(cursor)

    assert actual == 'Bank which serves the oldest client - Bank'


def test_get_bank_with_highest_outbound_users(cursor):
    cursor.fetchall.return_value = [('Bank1', 1), ('Bank1', 3), ('Bank2', 2)]
    cursor.fetchone.side_effect = [(1,), (2,), (3,)]

    actual = get_bank_with_highest_outbound_users.__wrapped__(cursor)

    assert actual == 'Bank with the highest users which performed outbound transactions - Bank1'


@pytest.mark.parametrize('table, message',
                         [
                             ('User', 'SELECT id FROM User WHERE Name IS NULL OR Surname IS NULL OR Birth_day IS NULL'),
                             ('Account', 'SELECT id FROM Account WHERE User_id IS NULL OR Type IS NULL '
                                         'OR Account_Number IS NULL OR Bank_id IS NULL OR '
                                         'Currency IS NULL OR Amount IS NULL OR Status IS NULL')
                         ])
def test_delete_users_or_accounts(table, message, cursor):
    cursor.fetchall.return_value = [(1,)]
    actual = delete_users_or_accounts(cursor, table)
    assert actual == [1]
    cursor.execute.assert_called_with(message)


@patch('api_module.delete_users_or_accounts')
@patch('api_module.delete_user')
@patch('api_module.delete_account')
def test_delete_users_and_accounts_with_missing_info(mock_a, mock_u, mock_f, cursor):
    mock_f.return_value = [1, 2]
    actual = delete_users_and_accounts_with_missing_info.__wrapped__(cursor)

    assert actual == 'Users and Accounts with missing information deleted successfully'


@patch('api_module.datetime')
@patch('api_module.check_availability')
def test_get_user_transactions_last_3_months(mock_f, mock_dt, cursor):
    name = 'aa aa'

    mock_dt.return_value = '2023-01-01'
    cursor.fetchone.return_value = (1,)
    cursor.fetchall.return_value = [(3, 'b', 1, 'ba', 2, 'USD', 100.0, '2023-08-22 11:51:01')]
    actual = get_user_transactions_last_3_months.__wrapped__(cursor, name)

    assert actual == [(3, 'b', 1, 'ba', 2, 'USD', 100.0, '2023-08-22 11:51:01')]
