import pandas as pd
import os

geo_dir = 'data/fuel_data_geo'
sweeping_geo_dir = 'data/fuel_data_geo_sweeping'

for filename in os.listdir(geo_dir):
    df = pd.read_csv(os.path.join(geo_dir, filename))

    df = df.loc[df['Pause_active'] != '1.0']

    df.to_csv(f'{os.path.join(sweeping_geo_dir, filename[:-4])}.csv', index=False)
