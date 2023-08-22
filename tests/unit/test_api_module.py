from unittest.mock import MagicMock, patch, call

from api_module import (get_users_with_debts, assign_random_discounts, get_bank_with_highest_outbound_users,
                        conversion_accounts, get_currency_and_amount, get_bank_name,
                        get_bank_with_largest_capital, get_bank_with_oldest_client,
                        get_user_transactions_last_3_months, delete_users, delete_accounts,
                        delete_users_and_accounts_with_missing_info, get_currency_conversion_rate,
                        transfer_money, check_availability)


def test_get_bank_name():
    cursor = MagicMock()

    acc_id = 1
    cursor.fetchone.return_value = ('Bank',)
    actual = get_bank_name.__wrapped__(cursor, acc_id)

    assert actual == 'Bank'


@patch('api_module.requests.get')
def test_get_currency_conversion_rate(mock_f):
    from_cur = 'USD'
    to_cur = 'EUR'
    mock_json = MagicMock(return_value={'data': {'EUR': 0.91}})
    mock_f.return_value.json = mock_json

    actual = get_currency_conversion_rate(from_cur, to_cur)

    assert 0.9 < actual < 1


def test_get_currency_and_amount():
    cursor = MagicMock()
    id = 1
    get_currency_and_amount(cursor, id)

    cursor.execute.assert_called_once_with('SELECT Currency, Amount FROM Account WHERE id = ?', (id,))


def test_check_availability():
    field = None
    error_message = 'Error'

    actual = check_availability(field, error_message)

    assert actual == 'Error'


@patch('api_module.get_currency_and_amount')
@patch('api_module.check_availability')
def test_conversion_accounts(mock_f, mock_c):
    cursor = MagicMock()
    mock_c.return_value = ('USD', 900)
    mock_f.return_value = None

    actual = conversion_accounts(cursor, 1, 2, 100)

    assert actual == (900, 'USD', 100)


@patch('api_module.conversion_accounts')
@patch('api_module.get_bank_name')
@patch('validations.validate_datetime')
def test_transfer_money(mock_dt, mock_bn, mock_f):
    cursor = MagicMock()

    sender_acc_id = 1
    receiver_account_id = 2
    amount = 200
    mock_dt.return_value = '2023-08-22 11:51:01'
    mock_bn.side_effect = ['Bank1', 'Bank2']

    cursor.execute.side_effect = [None, None, None]
    mock_f.return_value = 200, 'USD', 200
    actual = transfer_money.__wrapped__(cursor, sender_acc_id, receiver_account_id, amount)

    assert actual == 'Money transferred successfully'
    cursor.execute.assert_has_calls([call('UPDATE Account SET Amount = Amount - ? WHERE id = ?', (200, 1)),
                                     call('UPDATE Account SET Amount = Amount + ? WHERE id = ?', (200, 2)), ])


@patch('api_module.random.sample')
@patch('api_module.random.choice')
def test_assign_random_discounts(mock_random_sample, mock_random_choice):
    cursor = MagicMock()
    user_ids = [1, 2, 3, 4, 5]
    chosen_user_ids = [1, 3]

    cursor.execute.return_value = user_ids
    mock_random_sample.side_effect = [25, 50]
    mock_random_choice.return_value = chosen_user_ids

    actual = assign_random_discounts.__wrapped__(cursor)

    assert actual == {1: 25, 3: 50}


def test_get_users_with_debts():
    cursor = MagicMock()

    cursor.fetchall.side_effect = [[(1,)], [('Jo', 'aa')]]
    actual = get_users_with_debts.__wrapped__(cursor)

    assert actual == ['Jo aa']


def test_bank_with_largest_capital():
    cursor = MagicMock()

    cursor.fetchall.return_value = [(1, 100)]
    cursor.fetchone.return_value = ('Bank',)

    actual = get_bank_with_largest_capital.__wrapped__(cursor)
    assert actual == 'Bank which operates the biggest capital - Bank'


@patch('api_module.get_bank_name')
def test_get_bank_with_oldest_client(mock_f):
    cursor = MagicMock()

    cursor.fetchall.return_value = [('1990-01-01',), ('2000-01-01',)]
    cursor.fetchone.return_value = ('Bank',)
    mock_f.return_value = 'Bank'

    actual = get_bank_with_oldest_client.__wrapped__(cursor)

    assert actual == 'Bank which serves the oldest client - Bank'


def test_get_bank_with_highest_outbound_users():
    cursor = MagicMock()

    cursor.fetchall.return_value = [('Bank1', 1), ('Bank2', 2)]
    cursor.fetchone.side_effect = [(1,), (2,)]

    actual = get_bank_with_highest_outbound_users.__wrapped__(cursor)

    assert actual == 'Bank with the highest users which performed outbound transactions - Bank1'


@patch('table_manipulation.delete_user')
def test_delete_users(mock_f):
    cursor = MagicMock()

    cursor.fetchall.return_value = [(1,), (2,)]
    delete_users(cursor)

    cursor.execute.assert_called_once_with \
        ('SELECT id FROM User WHERE Name IS NULL OR Surname IS NULL OR Birth_day IS NULL')


@patch('table_manipulation.delete_account')
def test_delete_accounts(mock_f):
    cursor = MagicMock()

    cursor.fetchall.return_value = [(1,), (2,)]
    delete_accounts(cursor)

    cursor.execute.assert_called_once_with('SELECT id FROM Account WHERE User_id IS NULL OR Type IS NULL '
                                           'OR Account_Number IS NULL OR Bank_id IS NULL OR '
                                           'Currency IS NULL OR Amount IS NULL OR Status IS NULL ')


@patch('api_module.delete_accounts')
@patch('api_module.delete_users')
def test_delete_users_and_accounts_with_missing_info(mock_user, mock_acc):
    cursor = MagicMock()

    actual = delete_users_and_accounts_with_missing_info.__wrapped__(cursor)

    assert actual == 'Users and Accounts with missing information deleted successfully'


@patch('api_module.check_availability')
def test_get_user_transactions_last_3_months(mock_f):
    cursor = MagicMock()
    name = 'aa aa'

    cursor.fetchone.return_value = (1,)
    cursor.fetchall.return_value = [(3, 'b', 1, 'ba', 2, 'USD', 100.0, '2023-08-22 11:51:01')]
    actual = get_user_transactions_last_3_months.__wrapped__(cursor, name)

    assert actual == [(3, 'b', 1, 'ba', 2, 'USD', 100.0, '2023-08-22 11:51:01')]
