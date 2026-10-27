import pandas as pd
import joblib

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from sklearn.model_selection import train_test_split

# Load data
data = pd.read_csv("dataset/cleaned_dataset.csv")

X = data[["temperature", "humidity", "rainfall", "family_size"]]

y = data["water_used"]

# Load scaler
scaler = joblib.load("ml_model/scaler.pkl")

X = scaler.transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Load trained model
model = joblib.load("ml_model/model.pkl")

prediction = model.predict(X_test)

print("\nModel Evaluation")

print("--------------------------")

print("MAE :", mean_absolute_error(y_test,prediction))

print("MSE :", mean_squared_error(y_test,prediction))

print("R2 Score :", r2_score(y_test,prediction))