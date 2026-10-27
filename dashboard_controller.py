"""Dashboard controller - displays main dashboard with weather, predictions, and notifications."""
from flask import render_template, session, redirect, url_for, flash, jsonify
from services.weather_service import get_live_weather
from services.prediction_service import predict_water_usage, get_model_metrics
from services.notification_service import (
    generate_notifications, get_unread_notifications_count,
    get_notifications, mark_notification_as_read, mark_all_notifications_as_read
)
from database.db import get_connection


def dashboard():
    """Render the main dashboard page with auto-fetch forecast and notifications."""
    if "user_id" not in session:
        flash("Please login first", "danger")
        return redirect(url_for("auth.login"))

    city = session.get("city", "Coimbatore")
    user_id = session["user_id"]

    # Auto-fetch forecast and generate notifications for the user's city
    notification_result = generate_notifications(user_id, city)

    # Get weather data
    weather = get_live_weather(city)

    # Get model metrics
    metrics = get_model_metrics()

    # Get unread notifications count
    unread_count = get_unread_notifications_count(user_id)

    # Get recent notifications (top 5)
    recent_notifications = get_notifications(user_id, limit=5)

    # Get recent predictions
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT * FROM predictions 
           WHERE user_id=? 
           ORDER BY prediction_date DESC 
           LIMIT 5""",
        (user_id,)
    )
    recent_predictions = cursor.fetchall()
    conn.close()

    return render_template(
        "dashboard.html",
        weather=weather,
        metrics=metrics,
        predictions=recent_predictions,
        notifications=recent_notifications,
        unread_count=unread_count,
        notification_summary=notification_result,
        daily_rainfall=notification_result.get("daily_rainfall", []),
        fullname=session.get("fullname", "User"),
        city=city
    )


def mark_notification_read(notification_id):
    """Mark a single notification as read."""
    if "user_id" not in session:
        return jsonify({"status": "error", "message": "Not authenticated"}), 401
    
    success = mark_notification_as_read(notification_id, session["user_id"])
    if success:
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Notification not found"}), 404


def mark_all_read():
    """Mark all notifications as read."""
    if "user_id" not in session:
        return jsonify({"status": "error", "message": "Not authenticated"}), 401
    
    success = mark_all_notifications_as_read(session["user_id"])
    if success:
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Failed to update"}), 500


def get_notification_count():
    """Get unread notification count as JSON."""
    if "user_id" not in session:
        return jsonify({"count": 0})
    
    count = get_unread_notifications_count(session["user_id"])
    return jsonify({"count": count})