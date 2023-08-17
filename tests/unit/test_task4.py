import pytest
from unittest.mock import MagicMock, patch, mock_open
from datetime import datetime

from task4 import download_csv_file, filter_data, add_fields, create_folder_structure, calculate_max_age, \
    remove_decades_before_1960

TMP_DIR = 'test'


@pytest.fixture
def csv_file_path():
    csv_file_path = r'test\test_file.csv'

    with patch('builtins.open', new_callable=mock_open,
               read_data=('name,gender,dob.date,registered.date\n'
                          'John Doe,M,1990-01-01T00:00:00.000Z,2020-01-01T00:00:00.000Z\n'
                          'Jane Doe,F,1995-05-05T00:00:00.000Z,2021-05-05T00:00:00.000Z')):
        yield csv_file_path


@patch('task4.requests.get')
@patch('builtins.open', new_callable=mock_open)
def test_download_csv_file(mock_f, mock_open_func):
    response_mock = MagicMock()
    response_mock.text = 'name,gender,dob.date,registered.date\n' \
                         'John Doe,M,1990-01-01T00:00:00.000Z,' \
                         '2020-01-01T00:00:00.000Z'
    mock_f.return_value = response_mock

    filename = 'test_file'
    actual = download_csv_file(TMP_DIR, filename)
    expected = r'test\test_file.csv'

    mock_f.assert_called_once_with(r'test\test_file.csv', 'w', encoding='utf-8')
    assert actual == expected


@pytest.mark.parametrize('gender, rows, expected',
                         [
                             ('F', None, [{'name': 'Jane Doe', 'gender': 'F', 'dob.date': '1995-05-05T00:00:00.000Z',
                                           'registered.date': '2021-05-05T00:00:00.000Z'}]),
                             (None, 1, [{'name': 'John Doe', 'gender': 'M', 'dob.date': '1990-01-01T00:00:00.000Z',
                                         'registered.date': '2020-01-01T00:00:00.000Z'}])
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
    assert mock_f.call_count == 1
