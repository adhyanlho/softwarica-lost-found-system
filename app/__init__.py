from flask import Flask, flash, redirect, session, url_for
from flask_wtf.csrf import CSRFProtect
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 1. Initialize Global CSRF Protection
    csrf = CSRFProtect(app)

    # Set 5 MB maximum file upload limit
    app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

    from app.routes.auth import auth_bp
    from app.routes.main import main_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp)

    @app.route("/")
    def index():
        if "user_id" in session:
            return redirect(url_for("main.dashboard"))
        return redirect(url_for("auth.login"))

    # Security Headers Middleware
    @app.after_request
    def set_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response

    @app.errorhandler(413)
    def request_entity_too_large(error):
        flash("File is too large! Maximum allowed upload size is 5 MB.")
        return redirect(url_for("main.report"))

    return app