import os
import pandas as pd
import itertools

geo_data_dir = 'data/fuel_data_geo_sweeping'
geo_metrics_dir = 'results/geo_sweep_metrics'


total_unique_locations = []

# Average path length
truck_paths = []
# Total number of visits per unique location

# Define a function to count the repeated values in an array
def count_repeated_values(array):
    count_dict = {}
    for i in array:
        # If the element is already in the dictionary, increment its count
        if i in count_dict:
            count_dict[i] += 1
        # If the element is not in the dictionary, add it with a count of 1
        else:
            count_dict[i] = 1
    return count_dict


# Iterate over each file in the geographical data directory
for filename in os.listdir(geo_data_dir):
    df = pd.read_csv(os.path.join(geo_data_dir, filename))

    truck_path = []
    # Iterate over each location in the DataFrame
    for location in df['location']:
        # If the location is not already in the truck path, add it
        if location not in truck_path:
            truck_path.append(location)
        else:
            # If the location is not the same as the last location in the truck path, add it
            if location != truck_path[-1]:
                truck_path.append(location)
            else:
                continue

    # Get the unique locations visited by the truck
    visited_locations = df['location'].unique()

    with open(os.path.join(geo_metrics_dir, f'{filename[:-4]}.txt'), 'w') as f:

        f.write(f'{filename}\n\n')

        f.write(f'Number of unique locations sweeped: {len(visited_locations)}\n\n')

        f.write(f'Truck path: {len(truck_path)}\n')
        truck_paths.append(truck_path)
        
        # Write each location in the truck path to the file
        for loc in truck_path:
            f.write(f' {loc}\n')

        f.write('\n\nNumber of times each location was sweeped:\n')

        # Iterate over each location and its count in the truck path
        for label, value in count_repeated_values(truck_path).items():
            f.write(f'{label}: {value}\n')



with open(os.path.join(geo_metrics_dir, 'all_truck_paths.txt'), 'w') as f:
    f.write(f"Average number of locations sweeped: {sum([len(path) for path in truck_paths])/len(truck_paths)}\n\n")

    combined_path = list(itertools.chain(*truck_paths))
    unique_location_counts = count_repeated_values(combined_path)

    f.write(f'Total number of unique locations sweeped: {len(unique_location_counts)}\n\n')

    f.write(f'Number of times each location was sweeped:\n')
    for label, value in unique_location_counts.items():
        f.write(f'{label}: {value}\n')


