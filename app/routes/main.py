from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.database import get_connection


main_bp = Blueprint("main", __name__)


@main_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user_id = session.get("user_id")
    username = "User"
    items = []

    connection = get_connection()
    if connection is None:
        flash("Database connection failed. Please try again.")
        return render_template(
            "dashboard.html",
            username=username,
            items=items,
            lost_count=0,
            found_count=0,
            claimed_count=0,
            open_count=0,
        )

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT username FROM users WHERE id = %s",
            (user_id,),
        )
        user = cursor.fetchone()
        if user:
            username = user["username"]

        cursor.execute("SELECT * FROM items ORDER BY created_at DESC")
        items = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    lost_count = sum(1 for item in items if item["status"] == "lost")
    found_count = sum(1 for item in items if item["status"] == "found")
    claimed_count = sum(1 for item in items if item["status"] == "claimed")

    return render_template(
        "dashboard.html",
        username=username,
        items=items,
        lost_count=lost_count,
        found_count=found_count,
        claimed_count=claimed_count,
        open_count=lost_count + found_count,
    )


@main_bp.route("/report", methods=["GET", "POST"])
def report():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        category = request.form.get("category")
        status = request.form.get("status")
        location = request.form.get("location")

        connection = get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO items (title, description, category, status, location, user_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (title, description, category, status, location, session["user_id"]),
            )
            connection.commit()
        finally:
            cursor.close()
            connection.close()

        return redirect(url_for("main.dashboard"))

    return render_template("report.html")
