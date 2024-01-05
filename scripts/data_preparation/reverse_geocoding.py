import requests
import os
import pandas as pd

fuel_data_dir = 'data/fuel_data'

def get_address_from_coords(latitude, longitude):
    
    url = f'https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(data['display_name'])
        return data['display_name']
    else:
        print(f'Failed to fetch data for {latitude}, {longitude}')
        return 'Failed to fetch data'


for fuel_data_file in os.listdir(fuel_data_dir):
    df = pd.read_csv(os.path.join(fuel_data_dir, fuel_data_file))
    df['location'] = df.apply(lambda row: get_address_from_coords(row['Latitude'], row['Longitude']), axis=1)
    df.to_csv(os.path.join('data/fuel_data_geo', fuel_data_file), index=False)
    print("data file created")
