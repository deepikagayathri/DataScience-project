import os
from datetime import datetime

def save_prediction_report(city, prediction, weather):

    folder = "reports/prediction_reports"

    os.makedirs(folder, exist_ok=True)

    filename = datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".txt"

    filepath = os.path.join(folder, filename)

    with open(filepath, "w") as file:

        file.write("SMART WATER PREDICTION REPORT\n")
        file.write("=" * 40 + "\n\n")

        file.write(f"City : {city}\n")
        file.write(f"Temperature : {weather['temperature']} °C\n")
        file.write(f"Humidity : {weather['humidity']} %\n")
        file.write(f"Weather : {weather['condition']}\n")
        file.write(f"Predicted Water Consumption : {prediction} Liters\n")

    print("Prediction Report Saved Successfully")