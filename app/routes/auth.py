from app.extensions import limiter
from flask import Blueprint, redirect, session, url_for


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
@limiter.limit("3 per hour")
def register():
    from app.controllers.authController import register as register_controller

    return register_controller()


@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login():
    from app.controllers.authController import login as login_controller

    return login_controller()


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))