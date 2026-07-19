from flask import flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from app.database import get_connection


def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not username or not email or not password or not confirm_password:
            flash("All fields are required.")
            return render_template("register.html")

        if password != confirm_password:
            flash("Passwords do not match.")
            return render_template("register.html")

        password_hash = generate_password_hash(password)

        connection = get_connection()
        if connection is None:
            flash("Database connection failed. Please try again.")
            return render_template("register.html")

        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                (username, email, password_hash),
            )
            connection.commit()
        finally:
            cursor.close()
            connection.close()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for("auth.login"))

    return render_template("register.html")


def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Username and password are required.")
            return render_template("login.html")

        connection = get_connection()
        if connection is None:
            flash("Database connection failed. Please try again.")
            return render_template("login.html")

        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM users WHERE username = %s",
                (username,),
            )
            user = cursor.fetchone()
        finally:
            cursor.close()
            connection.close()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash("Login successful.")
            return redirect(url_for("main.dashboard"))

        flash("Invalid username or password.")
        return render_template("login.html")

    return render_template("login.html")


def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("auth.login"))
