import os
import pandas as pd
import matplotlib.pyplot as plt

fuel_data_dir = 'data/fuel_data'

total_fuel_consumptions = []
avg_fuel_consumptions = []
avg_engine_speeds = []
avg_fan_speeds = []
session_durations = []
pauses = []

for data_file in os.listdir(fuel_data_dir):

    try:
        # Load the data
        df = pd.read_csv(os.path.join(fuel_data_dir, data_file))

        # Calculate the total fuel consumed
        total_fuel_consumed = df['fuel_consumed'].sum()

        avg_fuel_consumed = df['fuel_consumed'].mean()

        # Fan speed is in RPM
        avg_fan_speed = df['FanSpeed'].mean()

        # Engine speed is in RPM
        avg_engine_speed = df['EngineSpeed'].mean()

        # Calculate the number of pauses
        num_of_pauses = df['Pause_active'].sum()

        # Convert 'time' column to datetime
        df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S.%f')

        # Calculate the difference in 'time' between the first and last row
        session_duration = (df['time'].iloc[-1] - df['time'].iloc[0]).total_seconds()

        total_fuel_consumptions.append(total_fuel_consumed)
        avg_fuel_consumptions.append(avg_fuel_consumed)
        session_durations.append(session_duration)
        avg_fan_speeds.append(avg_fan_speed)
        avg_engine_speeds.append(avg_engine_speed)
        pauses.append(num_of_pauses)

    except:
        continue


# Create subplots
fig, axs = plt.subplots(6, sharex=True, figsize=(20, 10))
fig.suptitle(f'Fuel consumption for all sessions', fontsize=16)

session_number = [i for i in range(1, len(total_fuel_consumptions) + 1)]

# Plot the data on the first subplot
axs[0].plot(session_number, avg_fuel_consumptions)
axs[0].set_title(f'Average Fuel Consumed')
axs[0].set_ylabel('Average Fuel Consumed [L]')

# Plot the data on the second subplot
axs[1].plot(session_number, total_fuel_consumptions)
axs[1].set_title(f'Total Fuel Consumption')
axs[1].set_ylabel('Total Fuel Consumed [L]')

# Plot the data on the second subplot
axs[2].plot(session_number, session_durations)
axs[2].set_title(f'Session Durations')
axs[2].set_ylabel('Session Durations')

# Plot the data on the second subplot
axs[3].plot(session_number, avg_fan_speeds)
axs[3].set_title(f'Average Fan Speeds')
axs[3].set_ylabel('Average Fan Speeds')

# Plot the data on the second subplot
axs[4].plot(session_number, avg_engine_speeds)
axs[4].set_title(f'Average Engine Speeds')
axs[4].set_ylabel('Average Engine Speeds')

# Plot the data on the second subplot
axs[5].plot(session_number, pauses)
axs[5].set_title(f'Pause_active')
axs[5].set_ylabel('Pause Active')
axs[5].set_xlabel('Session Number')

# Save the plot as an image file
plt.savefig(f'results/data_plots/all_sessions.png')