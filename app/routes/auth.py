from flask import Blueprint


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register_route():
    from app.controller.authController import register
    return register()


@auth_bp.route('/login', methods=['GET', 'POST'])
def login_route():
    from app.controller.authController import login
    return login()
