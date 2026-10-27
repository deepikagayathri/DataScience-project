"""Rainwater coverage page and rainfall data endpoints."""
from datetime import date, datetime, timedelta, timezone

from flask import flash, jsonify, redirect, render_template, request, session, url_for

from database.db import get_connection
from services.weather_service import get_live_weather
from weather.weather_api import get_forecast


def rainwater_coverage():
    """Render the rainfall chart shell; data is loaded from the JSON endpoints."""
    if "user_id" not in session:
        flash("Please login first", "danger")
        return redirect(url_for("auth.login"))

    city = session.get("city", "Coimbatore")

    return render_template(
        "rainwater_coverage.html",
        city=city,
        today=date.today().isoformat()
    )


def rainfall_history_api():
    """Return saved daily observations, collecting the latest live observation first."""
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    location = request.args.get("location", session.get("city", "Coimbatore")).strip()
    if not location:
        return jsonify({"error": "Location is required"}), 400

    current = get_live_weather(location)
    stored_location = current.get("city", location) if current.get("status") else location
    conn = get_connection()
    try:
        rows = conn.execute(
            """SELECT date, location, rainfall_mm, temperature, humidity, timestamp, data_type
               FROM rainfall_observations
               WHERE location=? COLLATE NOCASE AND data_type='observed'
               ORDER BY date ASC""",
            (stored_location,)
        ).fetchall()
    finally:
        conn.close()

    return jsonify({
        "location": stored_location,
        "today": current.get("date", date.today().isoformat()),
        "observations": [dict(row) for row in rows],
        "current_weather_available": bool(current.get("status"))
    })


def rainfall_forecast_api():
    """Return rainfall aggregated from real OpenWeather forecast intervals."""
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    location = request.args.get("location", session.get("city", "Coimbatore")).strip()
    if not location:
        return jsonify({"error": "Location is required"}), 400

    forecast = get_forecast(location)
    if not forecast:
        return jsonify({"location": location, "forecast": []})

    timezone_offset = forecast.get("city", {}).get("timezone", 0)
    local_today = (datetime.now(timezone.utc) + timedelta(seconds=timezone_offset)).date().isoformat()
    daily = {}
    for item in forecast.get("list", []):
        local_day = datetime.fromtimestamp(
            item["dt"] + timezone_offset, timezone.utc
        ).date().isoformat()
        if local_day <= local_today:
            continue
        day = daily.setdefault(local_day, {"rainfall": 0, "temperatures": [], "humidities": []})
        day["rainfall"] += item.get("rain", {}).get("3h", 0)
        day["temperatures"].append(item.get("main", {}).get("temp"))
        day["humidities"].append(item.get("main", {}).get("humidity"))

    fetched_at = datetime.now(timezone.utc).isoformat()
    conn = get_connection()
    try:
        for forecast_date, values in daily.items():
            temperatures = [value for value in values["temperatures"] if value is not None]
            humidities = [value for value in values["humidities"] if value is not None]
            conn.execute(
                """INSERT INTO rainfall_observations
                   (date, location, rainfall_mm, temperature, humidity, timestamp, data_type)
                   VALUES (?, ?, ?, ?, ?, ?, 'forecast')
                   ON CONFLICT(location, date, data_type) DO UPDATE SET
                       rainfall_mm=excluded.rainfall_mm,
                       temperature=excluded.temperature,
                       humidity=excluded.humidity,
                       timestamp=excluded.timestamp""",
                (
                    forecast_date, forecast.get("city", {}).get("name", location),
                    values["rainfall"],
                    sum(temperatures) / len(temperatures) if temperatures else None,
                    sum(humidities) / len(humidities) if humidities else None,
                    fetched_at
                )
            )
        conn.commit()
    finally:
        conn.close()

    return jsonify({
        "location": forecast.get("city", {}).get("name", location),
        "forecast": [
            {
                "date": forecast_date,
                "rainfall_mm": round(values["rainfall"], 2),
                "data_type": "forecast"
            }
            for forecast_date, values in sorted(daily.items())
        ]
    })