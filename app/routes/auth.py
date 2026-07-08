from flask import Blueprint


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    from app.controllers.authController import register as register_controller
    return register_controller()


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    from app.controllers.authController import login as login_controller
    return login_controller()


@auth_bp.route('/logout')
def logout():
    from app.controllers.authController import logout as logout_controller
    return logout_controller()
