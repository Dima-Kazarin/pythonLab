from unittest.mock import MagicMock

from table_manipulation import add_data_base, modify_base, delete_base


def test_add_data_base(cursor):
    data = ('Bank1',)

    actual = add_data_base(cursor, data, table='Bank', cols='(name)')

    assert actual == 'Data added successfully'
    cursor.execute.assert_called_once_with('INSERT INTO Bank (name) VALUES (?)', data)


def test_modify_base(cursor):
    id = 1
    field = 'name'
    mod_field = 'Jo'
    table = 'User'

    actual = modify_base(cursor, id, field, mod_field, table)

    assert actual == 'Data modified successfully'
    cursor.execute.assert_called_once_with('UPDATE User SET name = ? WHERE id = ?', (mod_field, id))


def test_delete_user(cursor):
    id = 1
    table = 'User'
    actual = delete_base(cursor, id, table)

    assert actual == 'Data deleted successfully'
    cursor.execute.assert_called_once_with('DELETE FROM User WHERE id = ?', (id,))
