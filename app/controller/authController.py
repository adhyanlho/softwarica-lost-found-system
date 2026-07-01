import mysql.connector
from flask import flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from app.database import get_connection


def register():
    if session.get("user_id"):
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        fullname = request.form.get("fullname", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        has_error = False

        if not fullname:
            flash("Full name is required.", "error")
            has_error = True

        if not email:
            flash("Email is required.", "error")
            has_error = True
        elif "@" not in email:
            flash("Please enter a valid email address.", "error")
            has_error = True

        if not password:
            flash("Password is required.", "error")
            has_error = True
        elif len(password) < 8:
            flash("Password must be at least 8 characters long.", "error")
            has_error = True

        if has_error:
            return render_template("register.html")

        conn = None
        cursor = None

        try:
            hashed_password = generate_password_hash(password)
            conn = get_connection()

            if conn is None:
                flash("Unable to connect to the database. Please try again later.", "error")
                return render_template("register.html")

            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (fullname, email, password, role) VALUES (%s, %s, %s, %s)",
                (fullname, email, hashed_password, "user"),
            )
            conn.commit()

            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("login"))

        except mysql.connector.Error:
            if conn:
                conn.rollback()
            flash("Registration failed. The email may already be registered.", "error")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    return render_template("register.html")


def login():
    if session.get("user_id"):
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        has_error = False

        if not email:
            flash("Email is required.", "error")
            has_error = True
        elif "@" not in email:
            flash("Please enter a valid email address.", "error")
            has_error = True

        if not password:
            flash("Password is required.", "error")
            has_error = True

        if has_error:
            return render_template("login.html")

        conn = None
        cursor = None

        try:
            conn = get_connection()

            if conn is None:
                flash("Unable to connect to the database. Please try again later.", "error")
                return render_template("login.html")

            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT id, fullname, email, password, role FROM users WHERE email = %s",
                (email,),
            )
            user = cursor.fetchone()

            if user and check_password_hash(user["password"], password):
                session.clear()
                session["user_id"] = user["id"]
                session["fullname"] = user["fullname"]
                session["role"] = user["role"]

                flash("Login successful.", "success")
                return redirect(url_for("dashboard"))

            flash("Invalid email or password.", "error")

        except mysql.connector.Error:
            flash("Login failed due to a database error. Please try again later.", "error")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    return render_template("login.html")
