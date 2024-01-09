import pandas as pd
import os

def calculate_metrics():
    """
    Calculate fuel consumption metrics for each session and save the results.

    This function reads fuel consumption data from multiple files, calculates metrics such as total fuel consumed,
    average fuel consumed per 100ms, standard deviation of fuel consumed, and session duration. The calculated metrics
    are then saved in separate files for each session, as well as in an aggregated file for all sessions.

    Args:
        None

    Returns:
        None
    """
    fuel_data_dir = 'data/fuel_data'
    single_session_results_dir = 'results/single_session_metrics'
    all_sessions_results_dir = 'results/all_sessions_metrics'

    total_fuel_consumptions = []
    avg_fuel_consumptions = []
    std_fuel_consumptions = []
    avg_engine_speeds = []
    std_engine_speeds = []
    avg_fan_speeds = []
    std_fan_speeds = []
    session_durations = []
    pauses = []

    for data_file in os.listdir(fuel_data_dir):

        try:
            # Load the data
            df = pd.read_csv(os.path.join(fuel_data_dir, data_file))

            # Calculate the total fuel consumed
            total_fuel_consumed = df['fuel_consumed'].sum()

            avg_fuel_consumed = df['fuel_consumed'].mean()

            std_fuel_consumed = df['fuel_consumed'].std()

            # Fan speed is in RPM
            avg_fan_speed = df['FanSpeed'].mean()

            std_fan_speed = df['FanSpeed'].std()

            # Engine speed is in RPM
            avg_engine_speed = df['EngineSpeed'].mean()

            std_engine_speed = df['EngineSpeed'].std()

            # Calculate the number of pauses
            num_of_pauses = df['Pause_active'].sum()

            # Convert 'time' column to datetime
            df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S.%f')

            # Calculate the difference in 'time' between the first and last row
            session_duration = (df['time'].iloc[-1] - df['time'].iloc[0]).total_seconds()

            print(f'{data_file} Fuel Consumed: {total_fuel_consumed} Mean Fuel Consumed : {avg_fuel_consumed} Std Fuel Consumed: {std_fuel_consumed} Duration: {session_duration}')
            
            # Save the results
            with open(os.path.join(single_session_results_dir, data_file), 'w') as f:
                f.write(f'Total Fuel Consumed: {total_fuel_consumed}\n')
                f.write(f'Average Fuel Consumed: {avg_fuel_consumed}\n')
                f.write(f'Std Fuel Consumed: {std_fuel_consumed}\n')
                f.write(f'Session Duration: {session_duration}\n')
                f.write(f'Average Fan Speed: {avg_fan_speed}\n')
                f.write(f'Std Fan Speed: {std_fan_speed}\n')
                f.write(f'Average Engine Speed: {avg_engine_speed}\n')
                f.write(f'Std Engine Speed: {std_engine_speed}\n')
                f.write(f'Number of Pauses: {num_of_pauses}\n')

            total_fuel_consumptions.append(total_fuel_consumed)
            avg_fuel_consumptions.append(avg_fuel_consumed)
            std_fuel_consumptions.append(std_fuel_consumed)
            session_durations.append(session_duration)
            avg_fan_speeds.append(avg_fan_speed)
            std_fan_speeds.append(std_fan_speed)
            avg_engine_speeds.append(avg_engine_speed)
            std_engine_speeds.append(std_engine_speed)
            pauses.append(num_of_pauses)

        except:
            continue

    # Save the results
    with open(os.path.join(all_sessions_results_dir, 'all_sessions_results.txt'), 'w') as f:
        f.write(f'Average Total Fuel Consumed: {sum(total_fuel_consumptions)/len(total_fuel_consumptions)}\n')
        f.write(f'Average Fuel Consumed: {sum(avg_fuel_consumptions)/len(avg_fuel_consumptions)}\n')
        f.write(f'Average Std Fuel Consumed: {sum(std_fuel_consumptions)/len(std_fuel_consumptions)}\n')
        f.write(f'Average Session Duration: {sum(session_durations)/len(session_durations)}\n')
        f.write(f'Average Fan Speed: {sum(avg_fan_speeds)/len(avg_fan_speeds)}\n')
        f.write(f'Average Std Fan Speed: {sum(std_fan_speeds)/len(std_fan_speeds)}\n')
        f.write(f'Average Engine Speed: {sum(avg_engine_speeds)/len(avg_engine_speeds)}\n')
        f.write(f'Average Std Engine Speed: {sum(std_engine_speeds)/len(std_engine_speeds)}\n')
        f.write(f'Average Number of Pauses: {sum(pauses)/len(pauses)}\n')

calculate_metrics()