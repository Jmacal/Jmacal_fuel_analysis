import pandas as pd
import os

def add_fuel_consumption():
    """
    Add fuel consumption column to each CSV file in the 'data/csv_files' directory.
    The fuel consumption is calculated based on the 'EngineFuelRateTMSCS' column.
    The modified CSV files are saved in the 'data/fuel_data' directory.
    """
    for csv_file in os.listdir('data/csv_files'):
        try:
            df = pd.read_csv(os.path.join('data/csv_files', csv_file))
            df['fuel_consumed'] = df['EngineFuelRateTMSCS'] * (0.1/3600)
            df.to_csv(os.path.join('data/fuel_data', csv_file), index=False)
        except:
            continue
