from flask import Blueprint, redirect, render_template, request, session, url_for

from app.database import get_connection


main_bp = Blueprint("main", __name__)


@main_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    return render_template("dashboard.html")


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
