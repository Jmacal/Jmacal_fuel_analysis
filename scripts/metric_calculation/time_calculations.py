import os
import pandas as pd


data_dir = 'data/fuel_data'
results_dir = 'results/time_metrics'

# Per activation, per 10min session, per day, per week, per month

# Nozzle1 down time
# Nozzle2 down time
# Fan on time
# Engine on time
# Fan speed
# Engine speed
# Fuel consumed

nozzle1_down_times = []
nozzle2_down_times = []
fan_on_times = []
engine_on_times = []
fan_speeds = []
engine_speeds = []
fuel_consumptions = []


# Per 10 min session
for data_file in os.listdir(data_dir):

    df = pd.read_csv(os.path.join(data_dir, data_file))
    print(df.head())

    # Nozzle1 Down

    nozzle1 = df[df['Nozzle1downTMSCS'] == 1.0]

    nozzle1_down_time = len(nozzle1) * 0.100

    avg_nozzle1_down_time = nozzle1_down_time / 600

    nozzle1_down_times.append(avg_nozzle1_down_time)

    # Nozzle2 Down

    nozzle2 = df[df['Nozzle2downTMS'] == 1.0]

    nozzle2_down_time = len(nozzle2) * 0.100

    avg_nozzle2_down_time = nozzle2_down_time / 600

    nozzle2_down_times.append(avg_nozzle2_down_time)

    # Fan ON

    fan = df[df['FanSpeed'] > 0.0]

    fan_on_time = len(fan) * 0.100

    avg_fan_on_time = fan_on_time / 600

    fan_on_times.append(avg_fan_on_time)

    avg_fan_speed = fan['FanSpeed'].mean()

    fan_speeds.append(avg_fan_speed)

    # Engine ON

    engine = df[df['EngineSpeed'] > 0.0]

    engine_on_time = len(engine) * 0.100

    avg_engine_on_time = engine_on_time / 600

    engine_on_times.append(avg_engine_on_time)

    avg_engine_speed = engine['EngineSpeed'].mean()

    engine_speeds.append(avg_engine_speed)

    # Fuel consumed
    print(os.path.join(data_dir, data_file))

    if not df.empty:
        fuel_consumed = df.iloc[-1]['TotalFuelConsumption'] - df.iloc[0]['TotalFuelConsumption']
        fuel_consumptions.append(fuel_consumed)
    else:
        print("DataFrame is empty")

print(fan_speeds)

nozzle1_down_time = sum(nozzle1_down_times) / len(nozzle1_down_times)
nozzle2_down_time = sum(nozzle2_down_times) / len(nozzle2_down_times)
fan_on_time = sum(fan_on_times) / len(fan_on_times)
engine_on_time = sum(engine_on_times) / len(engine_on_times)
fan_speed = sum(fan_speeds) / len(fan_speeds)
engine_speed = sum(engine_speeds) / len(engine_speeds)
fuel_consumed = sum(fuel_consumptions) / len(fuel_consumptions)

with open(os.path.join(results_dir, 'all_sessions_results.txt'), 'w') as f:
    f.write(f'Average Nozzle1 Down Time: {nozzle1_down_time}\n')
    f.write(f'Average Nozzle2 Down Time: {nozzle2_down_time}\n')
    f.write(f'Average Fan On Time: {fan_on_time}\n')
    f.write(f'Average Engine On Time: {engine_on_time}\n')
    f.write(f'Average Fan Speed: {fan_speed}\n')
    f.write(f'Average Engine Speed: {engine_speed}\n')
    f.write(f'Average Fuel Consumed: {fuel_consumed}\n')









