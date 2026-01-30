from typing import List
from datetime import datetime
from sqlalchemy import ForeignKey
from flask_login import UserMixin
from app.extensions import db

# Create user_acocunt table
class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    last_name = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    esr_number = db.Column(db.Integer, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    addresses = db.relationship("Address", back_populates="user", lazy=True)
    shifts = db.relationship("Shift", back_populates="user", lazy=True)

    def __repr__(self):
        return f"User(id={self.id}, username={self.username})"

# Create address table
class Address(db.Model):
    __tablename__ = "address"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120))
    user_id = db.Column(db.Integer, ForeignKey("user.id"))
    user = db.relationship("User", back_populates="addresses")

class Shift(db.Model):
    __tablename__ = "shifts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("user.id"))
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    summary = db.Column(db.String(100))
    user = db.relationship("User", back_populates="shifts")

