"""Report controller - generates and displays various reports."""
from flask import render_template, session, redirect, url_for, flash
from database.db import get_connection


def reports():
    """Display reports page with water usage statistics."""
    if "user_id" not in session:
        flash("Please login first", "danger")
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cursor = conn.cursor()

    # Total water usage
    cursor.execute("SELECT SUM(predicted_water_usage) FROM predictions WHERE user_id=?",
                   (session["user_id"],))
    total = cursor.fetchone()[0] or 0

    # Average prediction
    cursor.execute("SELECT AVG(predicted_water_usage) FROM predictions WHERE user_id=?",
                   (session["user_id"],))
    avg_usage = cursor.fetchone()[0] or 0

    # Prediction count
    cursor.execute("SELECT COUNT(*) FROM predictions WHERE user_id=?",
                   (session["user_id"],))
    count = cursor.fetchone()[0] or 0

    # Recent predictions
    cursor.execute(
        """SELECT * FROM predictions 
           WHERE user_id=? 
           ORDER BY prediction_date DESC 
           LIMIT 30""",
        (session["user_id"],)
    )
    recent = cursor.fetchall()

    chart_data = [
        {
            "date": row["prediction_date"][:10],
            "temperature": row["temperature"],
            "usage": row["predicted_water_usage"]
        }
        for row in reversed(recent)
    ]

    # Weather history count
    cursor.execute("SELECT COUNT(*) FROM weather_history")
    weather_count = cursor.fetchone()[0] or 0

    conn.close()

    return render_template(
        "reports.html",
        total=round(total, 2),
        avg_usage=round(avg_usage, 2),
        count=count,
        recent=recent,
        weather_count=weather_count,
        chart_data=chart_data
    )