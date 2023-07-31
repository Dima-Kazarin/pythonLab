import pytest
from unittest.mock import MagicMock, patch
import os
from datetime import datetime
from task4 import download_csv_file, filter_data, add_fields, create_folder_structure, calculate_max_age, \
    remove_decades_before_1960


@pytest.fixture
def csv_response_mock():
    response_mock = MagicMock()
    response_mock.text = 'name,gender,dob.date,registered.date\nJohn Doe,M,1990-01-01T00:00:00.000Z,' \
                         '2020-01-01T00:00:00.000Z\nJane Doe,F,1995-05-05T00:00:00.000Z,2021-05-05T00:00:00.000Z'
    return response_mock


@pytest.fixture
def csv_file_path(tmpdir):
    csv_file_path = os.path.join(tmpdir, 'test.csv')
    with open(csv_file_path, 'w', encoding='utf-8') as csv_file:
        csv_file.write('name,gender,dob.date,registered.date\nJohn Doe,M,1990-01-01T00:00:00.000Z,'
                       '2020-01-01T00:00:00.000Z\nJane Doe,F,1995-05-05T00:00:00.000Z,2021-05-05T00:00:00.000Z')
    return csv_file_path


@patch('task4.download_csv_file')
def test_download_csv_file(mock_f, csv_response_mock, tmpdir):
    mock_f.return_value = csv_response_mock
    filename = 'test_file'
    actual = download_csv_file(tmpdir, filename)
    assert os.path.exists(actual)
    assert os.path.isfile(actual)
    assert os.path.basename(actual) == f'{filename}.csv'


def test_filter_data_by_gender(csv_file_path):
    filtered_data = filter_data(csv_file_path, gender='M', rows=None)
    assert len(filtered_data) == 1
    assert filtered_data[0]['name'] == 'John Doe'


def test_filter_data_by_rows(csv_file_path):
    filtered_data = filter_data(csv_file_path, gender=None, rows=2)
    assert len(filtered_data) == 2
    assert filtered_data[0]['name'] == 'John Doe'
    assert filtered_data[1]['name'] == 'Jane Doe'


def test_add_fields():
    data = [{'dob.date': '1990-01-01T00:00:00.000Z',
             'registered.date': '2020-01-01T00:00:00.000Z', 'name.title': 'Mr', 'location.timezone.offset': '+05:30'}]
    add_fields(data)
    assert data[0]['global_index'] == 2
    assert data[0]['dob.date'] == '01/01/1990'
    assert data[0]['registered.date'] == '01-01-2020, 00:00:00'
    assert data[0]['name.title'] == 'mister'


def test_create_folder_structure():
    data = [{'dob.date': '01/01/1990', 'location.country': 'Country1'},
            {'dob.date': '05/05/1995', 'location.country': 'Country2'}]
    folder_structure = create_folder_structure(data)
    assert '1990-th' in folder_structure
    assert 'Country1' in folder_structure['1990-th']
    assert 'Country2' in folder_structure['1990-th']


def test_calculate_max_age():
    data = [{'dob.date': '01/01/1990'}, {'dob.date': '05/05/1995'}]
    max_age = calculate_max_age(data)
    assert max_age == datetime.today().year - 1990


def test_remove_decades_before_1960(tmpdir):
    folder_structure = {'1950-th': {}, '1960-th': {}}
    os.makedirs(os.path.join(tmpdir, '1950-th'))

    remove_decades_before_1960(tmpdir, folder_structure)
    assert '1950-th' not in folder_structure
    assert '1960-th' in folder_structure
