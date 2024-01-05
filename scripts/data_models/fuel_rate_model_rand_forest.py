from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
import numpy as np
import os
import joblib

model_path = 'results/model_weights/fuel_rate_model.pkl'
fuel_data = 'data/fuel_data'

if os.path.exists(model_path):
    # Load model
    model = joblib.load(model_path)
else:
    # Initialize a Random Forest Regressor
    model = RandomForestRegressor(n_estimators=100, random_state=42)


for data_file in os.listdir(fuel_data):
    data_file_path = os.path.join(fuel_data, data_file)

    try:
        # Load the data
        df = pd.read_csv(data_file_path)

        # Drops columns with missing values
        df = df.dropna(axis=1)

        df = df.drop('time', axis=1)

        # Identify categorical columns
        categorical_cols = df.select_dtypes(include=['object']).columns

        # One-hot encode categorical variables
        encoder = OneHotEncoder(sparse_output=False)
        encoded_data = encoder.fit_transform(df[categorical_cols])

        # Create a DataFrame from the encoded data
        encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(categorical_cols))

        # Drop the original categorical columns from df
        df = df.drop(categorical_cols, axis=1)

        # Concatenate the original DataFrame with the encoded DataFrame
        df = pd.concat([df, encoded_df], axis=1)

        # Normalize numerical variables
        scaler = MinMaxScaler()
        numerical_cols = ['Longitude', 'Latitude', 'Altitude', 'Satellites', 'Heading', 'EngineSpeed', 'RoadSpeedTMSCS', 'EngineFuelRateTMSCS', 'FanSpeed', 'TotalFuelConsumption', 'WaterTankLevel', 'pm_1', 'pm_2_5', 'pm_10', 'temperature', 'humidity']
        df[numerical_cols] = scaler.fit_transform(df[numerical_cols])

        # Prepare the data
        X = df.drop(['EngineFuelRateTMSCS'], axis=1)  # features
        y = df['EngineFuelRateTMSCS']  # target
        
        # Split the data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Fit the model with the training data
        model.fit(X_train, y_train)

        # Predict the target for the test data
        y_pred = model.predict(X_test)

        # Calculate the root mean squared error of the model
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        print(f'Root Mean Squared Error: {rmse}')

        # Calculate the accuracy of the model
        accuracy = model.score(X_test, y_test)
        print(f'Accuracy: {accuracy}')

        # Save the model
        joblib.dump(model, model_path)

        # Calculate the root mean squared error of the model
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        print(f'Root Mean Squared Error: {rmse}')
    except:
        print(f"Skipping empty file: {data_file}")
        continue

