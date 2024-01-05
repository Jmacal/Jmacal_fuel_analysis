import os
import pandas as pd
import matplotlib.pyplot as plt

def graph_fuel_consumption():
    """
    Graphs the fuel consumption data for each file in the 'data/fuel_data' directory.
    Saves the plots as image files in the 'results/data_plots' directory.
    """

    fuel_data = 'data/fuel_data'

    for data_file in os.listdir(fuel_data):
        try:
            # Read the data file
            df = pd.read_csv(os.path.join(fuel_data, data_file))

            # Convert the 'time' column to datetime format
            df['time'] = pd.to_datetime(df['time'])

            # Subtract the first time from each time entry to get the elapsed time
            df['time_elapsed'] = df['time'] - df['time'].iloc[0]

            # Convert the elapsed time to seconds
            df['time_elapsed'] = df['time_elapsed'].dt.total_seconds()

            # Create subplots
            fig, axs = plt.subplots(5, sharex=True, figsize=(30, 20))
            fig.suptitle(f'Fuel Consumption for {data_file[:-4]}', fontsize=16)

            # Plot the data on the first subplot
            axs[0].plot(df['time_elapsed'], df['fuel_consumed'])
            axs[0].set_title(f'Fuel Consumed')
            axs[0].set_ylabel('Fuel Consumed [L]')

            # Plot the data on the second subplot
            axs[1].plot(df['time_elapsed'], df['TotalFuelConsumption'])
            axs[1].set_title(f'Total Fuel Consumption')
            axs[1].set_ylabel('Total Fuel Consumed [L]')

            # Plot the data on the second subplot
            axs[2].plot(df['time_elapsed'], df['FanSpeed'])
            axs[2].set_title(f'FanSpeed')
            axs[2].set_ylabel('Fan Speed [RPM]')

            # Plot the data on the second subplot
            axs[3].plot(df['time_elapsed'], df['EngineSpeed'])
            axs[3].set_title(f'EngineSpeed')
            axs[3].set_ylabel('Engine Speed [RPM]')

            # Plot the data on the second subplot
            axs[4].plot(df['time_elapsed'], df['Pause_active'])
            axs[4].set_title(f'Pause_active')
            axs[4].set_ylabel('Pause Active')
            axs[4].set_xlabel('Time [s]')

            # Save the plot as an image file
            plt.savefig(f'results/data_plots/{data_file[:-4]}.png')

        except Exception as e:
            print(f"An error occurred: {e}")
            continue
