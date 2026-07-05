from flask import Flask, redirect, session, url_for
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    @app.route("/")
    def index():
        if "user_id" in session:
            return redirect(url_for("auth.login"))
        return redirect(url_for("auth.login"))

    return app
