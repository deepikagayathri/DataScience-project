import pandas as pd
import os

# Create dataset folder if it doesn't exist
os.makedirs("dataset", exist_ok=True)

# Read datasets
water = pd.read_csv("dataset/water_consumption.csv")
weather = pd.read_csv("dataset/weather_data.csv")

# Merge on date
data = pd.merge(water, weather, on="date")

# Remove missing values
data.dropna(inplace=True)

# Save cleaned dataset
data.to_csv("dataset/cleaned_dataset.csv", index=False)

print("✅ cleaned_dataset.csv created successfully!")
print(data.head())