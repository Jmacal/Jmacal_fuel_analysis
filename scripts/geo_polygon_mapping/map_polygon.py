import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Read the data
df = pd.read_csv('data/fuel_data_geo_sweeping/SN214929_2023_07_26_1154.csv')
lat_data = df['Latitude']
long_data = df['Longitude']

# # Fit a polynomial of degree 3 to the data
# coefficients = np.polyfit(long_data, lat_data, 3)

# # Create a polynomial function with the fitted coefficients
# polynomial = np.poly1d(coefficients)

# # Generate y-values for a range of x-values
# long_range = np.linspace(min(long_data), max(long_data), 100)
# lat_range = polynomial(long_range)

# # Plot the original data and the fitted polynomial
# plt.scatter(long_data, lat_data, label='Original data')
# plt.plot(long_range, lat_range, color='red', label='Fitted polynomial')
# plt.legend()
# plt.show()

from scipy.interpolate import make_interp_spline, BSpline

# Assume 't' is an array representing the order of the data points
t = np.arange(len(long_data))

# Fit a B-spline to the data as a function of 't'
degree = 61  # Degree of the spline. Change this value to adjust the flexibility of the fitted curve.
spl_lat = make_interp_spline(t, lat_data, k=degree)
spl_long = make_interp_spline(t, long_data, k=degree)

# Generate values for a range of 't'
t_range = np.linspace(min(t), max(t), 1000)
lat_range = spl_lat(t_range)
long_range = spl_long(t_range)

# Plot the original data and the fitted curve
plt.scatter(long_data, lat_data, color='blue', label='Original data')
plt.plot(long_range, lat_range, color='red', label='Fitted curve')
plt.legend()
plt.show()