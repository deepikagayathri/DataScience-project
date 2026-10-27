"""ML Model Training - Train multiple models and select the best one."""
import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def train_and_evaluate_models():
    """Train multiple ML models, evaluate them, and save the best one."""
    # Load cleaned dataset
    dataset_path = "dataset/cleaned_dataset.csv"
    if not os.path.exists(dataset_path):
        print(f"Dataset not found at {dataset_path}")
        return False

    data = pd.read_csv(dataset_path)
    data = data.dropna()

    # Features and target
    feature_columns = ["temperature", "humidity", "rainfall", "family_size"]
    X = data[feature_columns]
    y = data["water_used"]

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Save scaler
    joblib.dump(scaler, "ml_model/scaler.pkl")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    # Define models to evaluate
    models = {
        "Linear Regression": LinearRegression(),
        "Decision Tree": DecisionTreeRegressor(random_state=42),
        "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42)
    }

    best_model = None
    best_score = -float("inf")
    best_model_name = ""
    results = {}

    # Train and evaluate each model
    for name, model in models.items():
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        r2 = r2_score(y_test, predictions)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        mae = mean_absolute_error(y_test, predictions)

        results[name] = {
            "r2_score": round(r2, 4),
            "rmse": round(rmse, 4),
            "mae": round(mae, 4)
        }

        print(f"\n{name}:")
        print(f"  R² Score: {results[name]['r2_score']}")
        print(f"  RMSE: {results[name]['rmse']}")
        print(f"  MAE: {results[name]['mae']}")

        if r2 > best_score:
            best_score = r2
            best_model = model
            best_model_name = name

    # Save the best model
    joblib.dump(best_model, "ml_model/model.pkl")
    print(f"\n✅ Best Model: {best_model_name} with R² Score: {round(best_score, 4)}")
    print("✅ Model saved as ml_model/model.pkl")
    print("✅ Scaler saved as ml_model/scaler.pkl")

    # Save evaluation metrics to a file for reference
    metrics_df = pd.DataFrame(results).T
    metrics_df.to_csv("ml_model/model_metrics.csv")
    print("✅ Metrics saved to ml_model/model_metrics.csv")

    return True


if __name__ == "__main__":
    print("=" * 50)
    print("Smart Water Prediction - Model Training")
    print("=" * 50)
    train_and_evaluate_models()