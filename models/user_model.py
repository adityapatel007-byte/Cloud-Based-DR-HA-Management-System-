"""User model for authentication."""

from flask_login import UserMixin

from extensions import db


class User(db.Model, UserMixin):
    """System user account."""

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
