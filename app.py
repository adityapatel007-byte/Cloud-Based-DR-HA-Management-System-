"""Application entry point and factory."""

import os

from flask import Flask, current_app
from werkzeug.security import generate_password_hash

from config import Config
from extensions import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    """Load a user by ID for Flask-Login session handling."""
    from models.user_model import User

    return User.query.get(int(user_id))


def initialize_database():
    """Create database tables and ensure a default admin user exists."""
    from models.user_model import User

    db.create_all()

    username = current_app.config["ADMIN_DEFAULT_USERNAME"]
    existing_admin = User.query.filter_by(username=username).first()
    if existing_admin:
        return

    admin_user = User(
        username=username,
        password_hash=generate_password_hash(current_app.config["ADMIN_DEFAULT_PASSWORD"]),
    )
    db.session.add(admin_user)
    db.session.commit()


def register_cli_commands(app):
    """Register CLI helpers for operational tasks."""

    @app.cli.command("init-db")
    def init_db_command():
        """Initialize database tables and default data."""
        with app.app_context():
            initialize_database()
        print("Database initialized successfully.")


def register_blueprints(app):
    """Register all route blueprints."""
    from routes.auth_routes import auth_bp
    from routes.backup_routes import backup_bp
    from routes.dashboard_routes import dashboard_bp
    from routes.recovery_routes import recovery_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(backup_bp)
    app.register_blueprint(recovery_bp)


def create_app():
    """Create and configure the Flask application instance."""
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    register_blueprints(app)
    register_cli_commands(app)

    with app.app_context():
        initialize_database()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
