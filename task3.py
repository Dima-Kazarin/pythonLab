import os
import csv
import requests
import logging
import argparse
from datetime import datetime
import zipfile

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('logs.log')
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def download_csv_file(output_folder, filename):
    """
    Downloads a CSV file from a given URL and saves it in the specified output folder

    Parameters:
        output_folder (str): The path to the output folder where the file will be saved
        filename (str): The desired filename (without the extension) for the downloaded CSV file

    Returns:
        str: The path to the downloaded CSV file
    """
    url = 'https://randomuser.me/api/?results=5000&format=csv'
    response = requests.get(url)

    csv_file_path = os.path.join(output_folder, f'{filename}.csv')

    with open(csv_file_path, 'w', encoding='utf-8') as csv_file:
        csv_file.write(response.text)

    return csv_file_path


def filter_data(csv_file, gender, rows):
    """
    Filters the data from a CSV file based on gender and a specified number of rows

    Parameters:
        csv_file (str): The path to the CSV file to be filtered
        gender (str): The gender to filter by. If None, no gender filtering will be applied
        rows (int): The maximum number of rows to include in the filtered data. If None, all rows will be included

    Returns:
        list: A list of dictionaries representing the filtered data
    """
    filtered_data = []
    with open(csv_file, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if (not gender or row['gender'].lower() == gender.lower()) and (not rows or reader.line_num <= rows):
                filtered_data.append(row)

    return filtered_data


def add_fields(data):
    """
    Adds additional fields to the data

    Parameters:
        data (list): A list of dictionaries representing the data to which additional fields will be added
    """
    for row in data:
        row['global_index'] = row.get('index', '')

        dob_date = datetime.strptime(row['dob.date'], '%Y-%m-%dT%H:%M:%S.%fZ')
        row['dob.date'] = dob_date.strftime('%m/%d/%Y')

        reg_date = datetime.strptime(row['registered.date'], '%Y-%m-%dT%H:%M:%S.%fZ')
        row['registered.date'] = reg_date.strftime('%m-%d-%Y, %H:%M:%S')

        title_mapping = {
            'Mrs': 'missis',
            'Ms': 'miss',
            'Mr': 'mister',
            'Madame': 'mademoiselle'
        }
        row['name.title'] = title_mapping.get(row['name.title'])

        current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        row['current_time'] = current_time


def create_folder_structure(data):
    """
    Creates folder structure based on data

    Parameters:
        data (list): A list of dictionaries representing the data used to create the folder structure

    Returns:
        dict: A nested dictionary representing the folder structure
    """
    folder_structure = {}
    for row in data:
        dob_year = datetime.strptime(row['dob.date'], '%m/%d/%Y').year
        decade = f'{dob_year // 10}0-th'
        country = row['location.country']

        if decade not in folder_structure:
            folder_structure[decade] = {}
        if country not in folder_structure[decade]:
            folder_structure[decade][country] = []

        folder_structure[decade][country].append(row)

    return folder_structure


def calculate_max_age(data):
    """
    Calculates the maximum age from a list of data

    Parameters:
        data (list): A list of dictionaries representing the data containing date of birth information

    Returns:
        int: The maximum age calculated from the data
    """
    dob_dates = [datetime.strptime(row['dob.date'], '%m/%d/%Y') for row in data]
    today = datetime.today()
    max_age = max(today.year - date.year - ((today.month, today.day) < (date.month, date.day)) for date in dob_dates)
    return max_age


def calculate_avg_registered_years(data):
    """
    Calculates the average number of registered years from a list of data

    Parameters:
        data (list): A list of dictionaries representing the data containing registration date information

    Returns:
        float: The average number of registered years
    """
    reg_dates = [datetime.strptime(row['registered.date'], '%m-%d-%Y, %H:%M:%S') for row in data]
    today = datetime.today()
    avg_years = sum(
        today.year - date.year - ((today.month, today.day) < (date.month, date.day)) for date in reg_dates) / len(data)
    return avg_years


def calculate_popular_id(data):
    """
    Calculates the most popular id from a list of data

    Parameters:
        data (list): A list of dictionaries representing the data containing id information

    Returns:
        str: The most popular id
    """
    name_counts = {}
    for row in data:
        name = row['id.name']
        name_counts[name] = name_counts.get(name, 0) + 1
    popular_id = max(name_counts, key=name_counts.get)
    return popular_id


def create_folders(destination_folder, folder_structure):
    """
    Creates folders based on a nested dictionary representing folder structure

    Parameters:
        destination_folder (str): The path to the destination folder where the folders will be created
        folder_structure (dict): A nested dictionary representing the folder structure

    Returns:
        dict: The updated folder structure dictionary
    """
    for decade, countries in folder_structure.items():
        decade_folder = os.path.join(destination_folder, decade)
        os.makedirs(decade_folder, exist_ok=True)

        for country in countries:
            country_folder = os.path.join(decade_folder, country)
            os.makedirs(country_folder, exist_ok=True)

    return folder_structure


def store_data_to_files(destination_folder, folder_structure):
    """
    Stores data into CSV files within corresponding folders

    Parameters:
        destination_folder (str): The path to the destination folder where the CSV files will be stored
        folder_structure (dict): A nested dictionary representing the folder structure
    """
    for decade, countries in folder_structure.items():
        for country, users in countries.items():
            country_folder = os.path.join(destination_folder, decade, country)

            max_age = calculate_max_age(users)
            avg_registered_years = calculate_avg_registered_years(users)
            popular_id = calculate_popular_id(users)

            filename = f'max_age_{max_age}_avg_registered_{avg_registered_years:.2f}_popular_id_{popular_id}.csv'
            file_path = os.path.join(country_folder, filename)

            with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
                fieldnames = users[0].keys()
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(users)

            logger.info(f'Created file: {file_path}')


def remove_decades_before_1960(folder_structure):
    """
    Removes decades before the 1960s from the folder structure

    Parameters:
        folder_structure (dict): A nested dictionary representing the folder structure
    """
    decades_to_remove = [decade for decade in folder_structure.keys() if int(decade[:2]) < 60]

    for decade in decades_to_remove:
        del folder_structure[decade]


def log_structure_folder(destination_folder):
    """
    Logs the folder structure

    Parameters:
        destination_folder (str): The path to the destination folder whose structure will be logged
    """
    for foldername, subfolders, filenames in os.walk(destination_folder):
        logger.info(f'Folder: {os.path.relpath(foldername, destination_folder)}')
        for filename in filenames:
            logger.info(f'\t- File: {filename}')


def archive_destination_folder(destination_folder):
    """
    Archives the destination folder into a zip file

    Parameters:
        destination_folder (str): The path to the destination folder to be archived

    Returns:
        str: The path to the created zip file
    """
    zip_filename = f'{destination_folder}.zip'
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for foldername, subfolders, filenames in os.walk(destination_folder):
            for filename in filenames:
                filepath = os.path.join(foldername, filename)
                zipf.write(filepath, os.path.relpath(filepath, destination_folder))

    return zip_filename


def main():
    """
    Main function that orchestrates the data preparation process
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('destination_folder', help='Path to the output folder')
    parser.add_argument('--filename', default='output', help='The filename')
    parser.add_argument('--gender', help='Filter by gender')
    parser.add_argument('--rows', type=int, help='Number of rows')
    parser.add_argument('--log_level', default='INFO', help='Log level')

    args = parser.parse_args()

    logger.setLevel(getattr(logging, args.log_level.upper()))

    logger.info('Step 1: Starting data preparation process')

    logger.info('Step 2: Downloading CSV file')
    csv_file_path = download_csv_file(args.destination_folder, args.filename)

    logger.info('Step 3: Filtering data')
    filtered_data = filter_data(csv_file_path, args.gender, args.rows)

    logger.info('Step 4: Adding fields')
    add_fields(filtered_data)

    logger.info('Step 5: Creating folder structure')
    folder_structure = create_folder_structure(filtered_data)

    logger.info('Step 6: Creating the destination folder')
    os.makedirs(args.destination_folder, exist_ok=True)

    logger.info('Step 7: Moving the initial file to the destination folder')
    initial_file_path = os.path.join(args.destination_folder, f'{args.filename}.csv')
    os.replace(csv_file_path, initial_file_path)

    logger.info('Step 8: Creating folders for each decade and country')
    logger.info('Step 9: Creating subfolders for every decade')
    logger.info('Step 10: Creating subfolders for each country inside the decade folders')
    folder_structure = create_folders(args.destination_folder, folder_structure)

    logger.info('Step 11: Storing data to CSV files in corresponding folders')
    store_data_to_files(args.destination_folder, folder_structure)

    logger.info('Step 12: Removing data before the 1960s')
    remove_decades_before_1960(folder_structure)

    logger.info('Step 13: Logging folder structure')
    log_structure_folder(args.destination_folder)

    logger.info('Step 14: Archiving the destination folder')
    archive_filename = archive_destination_folder(args.destination_folder)
    logger.info(f'Archived the destination folder to: {archive_filename}')


if __name__ == '__main__':
    main()
