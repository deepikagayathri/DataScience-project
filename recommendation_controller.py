"""Recommendation controller - generates water-saving recommendations."""
from flask import render_template, request, session, redirect, url_for, flash
from services.recommendation_service import generate_recommendation
from services.weather_service import get_live_weather
from services.prediction_service import predict_water_usage


def recommendations():
    """Display water-saving recommendations based on weather and predictions."""
    if "user_id" not in session:
        flash("Please login first", "danger")
        return redirect(url_for("auth.login"))

    city = request.args.get("city", "Coimbatore")
    weather = get_live_weather(city)
    weather_condition = "clear"

    if weather and weather.get("status"):
        weather_condition = weather.get("condition", "clear").lower()

    # Get a sample prediction for recommendations
    temp = weather.get("temperature", 30) if weather and weather.get("status") else 30
    humidity = weather.get("humidity", 60) if weather and weather.get("status") else 60
    rainfall = weather.get("rainfall", 0) if weather and weather.get("status") else 0

    prediction = predict_water_usage(temp, humidity, rainfall, 4)
    predicted_value = prediction.get("prediction", 200) if prediction.get("status") else 200

    recommendations_list = generate_recommendation(weather_condition, predicted_value)

    return render_template(
        "recommendations.html",
        recommendations=recommendations_list,
        weather=weather,
        predicted_usage=predicted_value,
        city=city
    )