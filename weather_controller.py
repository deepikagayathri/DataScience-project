"""Weather controller - handles weather display and city search."""
from flask import render_template, request, session, redirect, url_for, flash
from services.weather_service import get_live_weather
from weather.weather_api import get_forecast
from weather.weather_parser import parse_weather
from database.db import get_connection
from datetime import datetime


def weather():
    """Display weather page with city search."""
    if "user_id" not in session:
        flash("Please login first", "danger")
        return redirect(url_for("auth.login"))

    city = request.args.get("city", "Coimbatore")
    weather_data = get_live_weather(city)
    forecast_data = None

    # Get forecast
    forecast_raw = get_forecast(city)
    if forecast_raw:
        forecast_data = parse_weather(forecast_raw)

    # Save weather to history
    if weather_data and weather_data.get("status"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO weather_history 
               (city, temperature, humidity, pressure, wind_speed, weather, description, rainfall)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                weather_data.get("city", city),
                weather_data.get("temperature", 0),
                weather_data.get("humidity", 0),
                weather_data.get("pressure", 0),
                weather_data.get("wind_speed", 0),
                weather_data.get("condition", "N/A"),
                weather_data.get("description", ""),
                weather_data.get("rainfall", 0)
            )
        )
        conn.commit()
        conn.close()

    return render_template(
        "weather.html",
        weather=weather_data,
        forecast=forecast_data,
        city=city
    )