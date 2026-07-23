import os
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename

from app.database import get_connection

main_bp = Blueprint("main", __name__)


@main_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user_id = session.get("user_id")
    username = "User"
    user_role = "user"
    is_admin = False
    items = []

    connection = get_connection()
    if connection is None:
        flash("Database connection failed. Please try again.")
        return render_template(
            "dashboard.html",
            username=username,
            user_role=user_role,
            is_admin=False,
            items=items,
            lost_count=0,
            found_count=0,
            claimed_count=0,
            open_count=0,
        )

    search_query = request.args.get("search", "").strip()
    category_filter = request.args.get("category", "").strip()

    cursor = connection.cursor(dictionary=True)
    try:
        # Fetch username and role from database
        cursor.execute(
            "SELECT username, role FROM users WHERE id = %s",
            (user_id,),
        )
        user = cursor.fetchone()
        if user:
            username = user.get("username", "User")
            user_role = str(user.get("role", "user")).strip().lower()

        is_admin = (user_role == "admin")

        cursor.execute("SELECT status FROM items")
        stats_data = cursor.fetchall()
        lost_count = sum(1 for item in stats_data if item["status"] == "lost")
        found_count = sum(1 for item in stats_data if item["status"] == "found")
        claimed_count = sum(1 for item in stats_data if item["status"] == "claimed")

        # Admin sees all items; standard users see approved items OR items they uploaded themselves
        query_params = []
        if is_admin:
            query_string = "SELECT * FROM items WHERE 1=1"
        else:
            query_string = "SELECT * FROM items WHERE (is_approved = 1 OR user_id = %s)"
            query_params.append(user_id)

        if search_query:
            query_string += " AND (title LIKE %s OR description LIKE %s)"
            query_params.extend([f"%{search_query}%", f"%{search_query}%"])

        if category_filter and category_filter.lower() != "all":
            query_string += " AND category = %s"
            query_params.append(category_filter)

        query_string += " ORDER BY created_at DESC"

        cursor.execute(query_string, tuple(query_params))
        items = cursor.fetchall()

    finally:
        cursor.close()
        connection.close()

    return render_template(
        "dashboard.html",
        username=username,
        user_role=user_role,
        is_admin=is_admin,
        items=items,
        lost_count=lost_count,
        found_count=found_count,
        claimed_count=claimed_count,
        open_count=lost_count + found_count,
        search_query=search_query,
        category_filter=category_filter,
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

        image_file = request.files.get("image")
        image_url = None

        if image_file and image_file.filename != "":
            filename = secure_filename(image_file.filename)

            upload_dir = os.path.join("app", "static", "uploads")
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)

            image_file.save(os.path.join(upload_dir, filename))
            image_url = f"uploads/{filename}"

        connection = get_connection()
        if connection is None:
            flash("Database connection failed.")
            return redirect(url_for("main.dashboard"))

        cursor = connection.cursor()
        try:
            # Set is_approved to 0 so new reports require admin moderation
            cursor.execute(
                """
                INSERT INTO items (title, description, category, status, location, image_url, user_id, is_approved)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 0)
                """,
                (title, description, category, status, location, image_url, session["user_id"]),
            )
            connection.commit()
            flash("Item reported successfully! Pending admin approval.")
        finally:
            cursor.close()
            connection.close()

        return redirect(url_for("main.dashboard"))

    return render_template("report.html")


@main_bp.route("/item/<int:item_id>")
def view_item(item_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    connection = get_connection()
    if connection is None:
        flash("Database connection error.")
        return redirect(url_for("main.dashboard"))

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT items.*, users.username AS reporter_name 
            FROM items 
            JOIN users ON items.user_id = users.id 
            WHERE items.id = %s
            """,
            (item_id,),
        )
        item = cursor.fetchone()
    finally:
        cursor.close()
        connection.close()

    if not item:
        flash("Item not found.")
        return redirect(url_for("main.dashboard"))

    is_owner = item["user_id"] == session["user_id"]

    return render_template("view_item.html", item=item, is_owner=is_owner)


@main_bp.route("/item/<int:item_id>/reclaim", methods=["POST"])
def reclaim_item(item_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    connection = get_connection()
    if connection is None:
        flash("Database connection error.")
        return redirect(url_for("main.dashboard"))

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT user_id FROM items WHERE id = %s", (item_id,))
        item = cursor.fetchone()

        if not item:
            flash("Item not found.")
            return redirect(url_for("main.dashboard"))

        if item["user_id"] != session["user_id"]:
            flash("Access denied. You do not own this record.")
            return redirect(url_for("main.dashboard")), 403

        cursor.execute(
            "UPDATE items SET status = 'claimed' WHERE id = %s",
            (item_id,),
        )
        connection.commit()
        flash("Item successfully updated to Reclaimed!")
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for("main.dashboard"))


@main_bp.route("/admin/approve/<int:item_id>", methods=["POST"])
def approve_item(item_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    connection = get_connection()
    if connection is None:
        flash("Database connection error.")
        return redirect(url_for("main.dashboard"))

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT role FROM users WHERE id = %s", (session["user_id"],))
        user = cursor.fetchone()
        if not user or str(user.get("role", "")).strip().lower() != "admin":
            flash("Access denied. Admin privileges required.", "error")
            return redirect(url_for("main.dashboard")), 403

        cursor.execute("UPDATE items SET is_approved = 1 WHERE id = %s", (item_id,))
        connection.commit()
        flash("Item approved and published successfully!", "success")
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for("main.dashboard"))


@main_bp.route("/admin/delete/<int:item_id>", methods=["POST"])
def delete_item(item_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    connection = get_connection()
    if connection is None:
        flash("Database connection error.")
        return redirect(url_for("main.dashboard"))

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT role FROM users WHERE id = %s", (session["user_id"],))
        user = cursor.fetchone()
        if not user or str(user.get("role", "")).strip().lower() != "admin":
            flash("Access denied. Admin privileges required.", "error")
            return redirect(url_for("main.dashboard")), 403

        cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
        connection.commit()
        flash("Item removed successfully.", "success")
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for("main.dashboard"))