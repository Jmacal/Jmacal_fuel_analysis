from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import pandas as pd
import numpy as np
import os
import joblib

model_exists = False

model_path = 'results/model_weights/fuel_rate_model_LSTM.pkl'
fuel_data = 'data/fuel_data'

if os.path.exists(model_path):
    # Load model
    model = joblib.load(model_path)
    print("test")
    model_exists = True
else:
    # Initialize a LSTM model
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(1, 48)))  # Update input_shape to match the number of features
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])

for fuel_data_file in os.listdir(fuel_data):
    fuel_data_path = os.path.join(fuel_data, fuel_data_file)

    # try:
    # Load the data
    df = pd.read_csv(fuel_data_path)

    # Drops columns with missing values
    #df = df.dropna(axis=1)

    df = df.drop(['GutterSprayOnOff', 'AddWaterSprayOnOff', 'WaterRe_circOnOff'], axis=1)

    # Convert 'time' column to datetime
    df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S.%f')

    # Convert 'time' column to Unix time
    df['time'] = df['time'].apply(lambda x: x.timestamp())

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
    numerical_cols = ['time', 'Longitude', 'Latitude', 'Altitude', 'Satellites', 'Heading', 'EngineSpeed', 'RoadSpeedTMSCS', 'EngineFuelRateTMSCS', 'FanSpeed', 'TotalFuelConsumption', 'WaterTankLevel', 'pm_1', 'pm_2_5', 'pm_10', 'temperature', 'humidity']
    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])

    # Prepare the data
    X = df.drop(['EngineFuelRateTMSCS'], axis=1)  # features

    y = df['EngineFuelRateTMSCS']  # target

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Reshape input to be 3D [samples, timesteps, features]
    X_train = X_train.values.reshape((X_train.shape[0], 1, X_train.shape[1]))
    X_test = X_test.values.reshape((X_test.shape[0], 1, X_test.shape[1]))

    # Fit the model with the training data
    model.fit(X_train, y_train, epochs=50, verbose=0)

    # Predict the target for the test data
    y_pred = model.predict(X_test)

    model.compile(optimizer='adam', loss='mse', metrics=['mae'])

    loss, mae = model.evaluate(X_test, y_test)
    print(f'Loss: {loss}')
    print(f'Mean Absolute Error: {mae}')

    if model_exists:
        # Add feature importance code below

        input_lstm_weights = model.layers[0].get_weights()[0]  # Get input weights
        feature_importance = np.mean(np.abs(input_lstm_weights), axis=1)
        
        # feature_importance now contains importance scores for each feature

        # Mapping importance scores to feature names
        feature_names = X.columns  # Assuming X is a DataFrame
        importance_dict = dict(zip(feature_names, feature_importance))

        # Sorting features by importance
        sorted_importance = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)

        # Displaying sorted feature importance
        for feature, importance in sorted_importance:
            print(f"Feature: {feature}, Importance: {importance}")
    
        break

    # Save the model
    joblib.dump(model, model_path)

    # except:
    #     print(f"Skipping empty file: {csv_file}")
    #     continue

