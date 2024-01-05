import os
import csv

def convert_log_files_to_csv():
    """
    Converts log files to CSV format.

    Reads log files from the specified data folder, extracts data, and saves it as CSV files.
    Each log file is converted to a separate CSV file with the same name.

    Args:
        None

    Returns:
        None
    """
    output_csv_dir = 'data/csv_files'
    fuel_data_dirs = ['data/log_files']

    for data_folder in fuel_data_dirs:
        for file in os.listdir(data_folder):
            columns = []
            data = []
            reading_data = False

            with open(os.path.join(data_folder, file), 'r') as data_file:
                for row in data_file:
                    if row.split(' ')[0] == 'time':
                        columns = row.split(' ')
                    elif row.split(']')[0] == '[data':
                        reading_data = True
                        continue

                    if reading_data:
                        data_row = row.split(' ')
                        data.append(data_row)

            with open(os.path.join('data/', output_csv_dir, file), 'w') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=',')
                csv_writer.writerow(columns)
                for d_r in data:
                    csv_writer.writerow(d_r)


