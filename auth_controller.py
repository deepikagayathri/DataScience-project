"""Authentication controller - handles login, register, logout, and profile."""
from flask import render_template, request, redirect, url_for, flash, session
from database.db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash


def login():
    """Handle user login."""
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["fullname"] = user["fullname"]
            session["email"] = user["email"]
            session["city"] = user["city"] if user["city"] else "Coimbatore"
            flash("Login successful!", "success")
            return redirect(url_for("dashboard.dashboard"))

        flash("Invalid email or password", "danger")
        return redirect(url_for("auth.login"))

    return render_template("login.html")


def register():
    """Handle user registration with preferred city."""
    if request.method == "POST":
        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        city = request.form.get("city", "Coimbatore")

        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return redirect(url_for("auth.register"))

        if len(password) < 6:
            flash("Password must be at least 6 characters", "danger")
            return redirect(url_for("auth.register"))

        hashed_password = generate_password_hash(password)

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (fullname, email, password, city) VALUES (?, ?, ?, ?)",
                (fullname, email, hashed_password, city)
            )
            conn.commit()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("auth.login"))
        except Exception as e:
            flash("Email already exists!", "danger")
            return redirect(url_for("auth.register"))
        finally:
            conn.close()

    return render_template("register.html")


def logout():
    """Handle user logout."""
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))


def profile():
    """Display user profile page."""
    if "user_id" not in session:
        flash("Please login first", "danger")
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE id=?",
        (session["user_id"],)
    )
    user = cursor.fetchone()
    conn.close()

    return render_template("profile.html", user=user)


def update_city():
    """Update user's preferred city."""
    if "user_id" not in session:
        flash("Please login first", "danger")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        city = request.form.get("city", "Coimbatore")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET city=? WHERE id=?",
            (city, session["user_id"])
        )
        conn.commit()
        conn.close()
        session["city"] = city
        flash("City updated successfully!", "success")
        return redirect(url_for("dashboard.dashboard"))