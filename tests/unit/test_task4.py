import pytest
from unittest.mock import MagicMock, patch, mock_open
from datetime import datetime

from task4 import download_csv_file, filter_data, add_fields, create_folder_structure, calculate_max_age, \
    remove_decades_before_1960

TMP_DIR = 'test'
TEST_USER_2 = {'name': 'Jane Doe', 'gender': 'F', 'dob.date': '1995-05-05T00:00:00.000Z',
               'registered.date': '2021-05-05T00:00:00.000Z'}

TEST_USER_1 = {'name': 'John Doe', 'gender': 'M', 'dob.date': '1990-01-01T00:00:00.000Z',
               'registered.date': '2020-01-01T00:00:00.000Z'}


@pytest.fixture
def user_1_str_and_user_2_str():
    user_1_str = ','.join(TEST_USER_1.values())
    user_2_str = ','.join(TEST_USER_2.values())
    return user_1_str, user_2_str


@pytest.fixture
def header():
    return ','.join(TEST_USER_2.keys())


@pytest.fixture
def csv_file_path(user_1_str_and_user_2_str, header):
    csv_file_path = r'test\test_file.csv'

    user_1, user_2 = user_1_str_and_user_2_str
    with patch('builtins.open', new_callable=mock_open,
               read_data=f'{header}\n{user_1}\n{user_2}'):
        yield csv_file_path


@patch('task4.get')
@patch('builtins.open', new_callable=mock_open)
def test_download_csv_file(mock_f, mock_open_func, user_1_str_and_user_2_str, header):
    response_mock = MagicMock()
    user_1, _ = user_1_str_and_user_2_str
    response_mock.text = f'{header}\n{user_1}'
    mock_f.return_value = response_mock

    filename = 'test_file'
    actual = download_csv_file(TMP_DIR, filename)
    expected = r'test\test_file.csv'

    mock_f.assert_called_once_with(r'test\test_file.csv', 'w', encoding='utf-8')
    assert actual == expected


@pytest.mark.parametrize('gender, rows, expected',
                         [
                             ('F', None, [TEST_USER_2]),
                             (None, 1, [TEST_USER_1])
                         ])
def test_filter_data(csv_file_path, gender, rows, expected):
    filtered_data = filter_data(csv_file_path, gender=gender, rows=rows)

    assert filtered_data == expected


@patch('task4.datetime', MagicMock(now=lambda tz=None: datetime(2023, 8, 17, 12, 0, 0, tzinfo=tz),
                                   strptime=lambda date_string, format_str: datetime.strptime(date_string, format_str)))
def test_add_fields():
    data = [{'dob.date': '1990-01-01T00:00:00.000Z',
             'registered.date': '2020-01-01T00:00:00.000Z', 'name.title': 'Mr', 'location.timezone.offset': '+05:30'}]
    add_fields(data)

    expected = [{'global_index': 2, 'location.timezone.offset': '+05:30', 'dob.date': '01/01/1990',
                 'registered.date': '01-01-2020, 00:00:00', 'name.title': 'mister',
                 'current_time': '2023-08-17 12:00:00'}]

    assert data == expected


def test_create_folder_structure():
    data = [{'dob.date': '01/01/1990', 'location.country': 'Country1'},
            {'dob.date': '05/05/1995', 'location.country': 'Country2'},
            {'dob.date': '05/05/1961', 'location.country': 'Country3'}]
    folder_structure = create_folder_structure(data)

    expected = {'1960-th': {'Country3': [{'dob.date': '05/05/1961',
                                          'location.country': 'Country3'}]},
                '1990-th': {'Country1': [{'dob.date': '01/01/1990',
                                          'location.country': 'Country1'}],
                            'Country2': [{'dob.date': '05/05/1995',
                                          'location.country': 'Country2'}]}}
    assert folder_structure == expected


def test_calculate_max_age():
    data = [{'dob.date': '01/01/1990'}, {'dob.date': '05/05/1995'}]
    max_age = calculate_max_age(data)
    expected = 33
    assert max_age == expected


@patch('task4.shutil.rmtree')
def test_remove_decades_before_1960(mock_f):
    folder_structure = {'1950-th': {}, '1960-th': {}}

    remove_decades_before_1960(TMP_DIR, folder_structure)
    expected = {'1960-th': {}}

    assert folder_structure == expected
    mock_f.assert_called_once_with(r'test\1950-th')
