data_dir = 'data/fuel_data'

for data_file in os.listdir(data_dir):
    df = pd.read_csv(os.path.join(data_dir, data_file))

    df = [df['Pause_active'] == 0.0]
    df = df[df['FanOnTMS'] == 1.0]
    df = df[df['EngineSpeed'] > 0.0]
    df = df[df['FanSpeed'] > 0.0]
    df = df[df['Nozzle1downTMSCS'] == 1.0 or df['Nozzle2downTMSCS'] == 1.0 and df['SideBrush2DownTMS'] == 1.0 ]
    


   



    df.to_csv(os.path.join(data_dir, data_file), index=False)