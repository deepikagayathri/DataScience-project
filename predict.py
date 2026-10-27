import joblib

# Load model
model = joblib.load("ml_model/model.pkl")

# Load scaler
scaler = joblib.load("ml_model/scaler.pkl")

temperature = float(input("Temperature (°C): "))
humidity = float(input("Humidity (%): "))
rainfall = float(input("Rainfall (mm): "))

sample = [[temperature, humidity, rainfall]]

sample = scaler.transform(sample)

prediction = model.predict(sample)

print("\nPredicted Water Consumption")

print("--------------------------------")

print(round(prediction[0],2),"Liters")