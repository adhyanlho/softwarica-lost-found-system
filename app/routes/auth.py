from flask import Blueprint

from app.controller.authController import login, register


auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register_route():
    return register()


@auth_bp.route("/login", methods=["GET", "POST"])
def login_route():
    return login()
