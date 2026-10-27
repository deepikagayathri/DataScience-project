"""Prediction controller - handles ML prediction requests."""
from flask import render_template, request, session, redirect, url_for, flash, jsonify
from services.prediction_service import predict_water_usage, get_model_metrics
from database.db import get_connection


def _environmental_alert(temperature, humidity, rainfall):
    """Create a simple explanation for the environmental conditions."""
    high_temperature = temperature >= 32
    low_humidity = humidity <= 40
    high_humidity = humidity >= 70
    low_rainfall = rainfall <= 2
    high_rainfall = rainfall >= 10
    moderate_temperature = 20 <= temperature < 32
    moderate_humidity = 40 < humidity < 70

    if high_temperature and low_humidity and low_rainfall:
        message = (
            "High water demand condition: Temperature is high, humidity is low, "
            "and rainfall is low. Water consumption may increase."
        )
        condition = "High Water Demand"
    elif high_rainfall:
        message = (
            "Rainfall Alert: Good rainfall is available, which may reduce the need "
            "for some outdoor water usage."
        )
        condition = "Lower Outdoor Water Demand"
    elif high_humidity:
        message = "High Humidity: Humidity is high, so outdoor water demand may be lower."
        condition = "Low to Moderate Water Demand"
    elif moderate_temperature and moderate_humidity and rainfall > 0:
        message = "Favorable Water Condition: Moderate temperature and humidity with rainfall availability."
        condition = "Moderate Water Demand"
    elif high_temperature or low_rainfall:
        message = "Water demand may be higher because the weather is warm or rainfall is limited."
        condition = "Moderate to High Water Demand"
    else:
        message = "The current weather conditions suggest a normal level of water demand."
        condition = "Moderate Water Demand"

    return {
        "message": message,
        "condition": condition,
        "values": f"Temperature: {temperature:g}°C | Humidity: {humidity:g}% | Rainfall: {rainfall:g} mm"
    }


def prediction():
    """Handle prediction form submission and display."""
    if "user_id" not in session:
        flash("Please login first", "danger")
        return redirect(url_for("auth.login"))

    prediction_result = None
    environmental_alert = None
    metrics = get_model_metrics()

    if request.method == "POST":
        try:
            required_fields = ["temperature", "humidity", "rainfall", "family_size"]
            if any(not request.form.get(field, "").strip() for field in required_fields):
                raise ValueError("All input fields are required")

            temperature = float(request.form["temperature"])
            humidity = float(request.form["humidity"])
            rainfall = float(request.form["rainfall"])
            family_size = int(request.form["family_size"])

            environmental_alert = _environmental_alert(temperature, humidity, rainfall)

            prediction_result = predict_water_usage(
                temperature, humidity, rainfall, family_size
            )

            # Save prediction to database
            if prediction_result["status"]:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    """INSERT INTO predictions 
                       (user_id, temperature, humidity, rainfall, family_size, predicted_water_usage)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (session["user_id"], temperature, humidity, rainfall,
                     family_size, prediction_result["prediction"])
                )
                conn.commit()
                conn.close()

        except ValueError as error:
            message = str(error) or "Please enter valid numeric values"
            flash(message, "danger")
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")

    return render_template(
        "prediction.html",
        result=prediction_result,
        metrics=metrics,
        environmental_alert=environmental_alert
    )