from flask import Blueprint, redirect, session, url_for


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
    session.clear()
    return redirect(url_for('auth.login'))
