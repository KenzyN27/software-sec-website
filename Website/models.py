from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    # have a separate ID as primary key instead of the email due to uniqueness/scecurity
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(320), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(71), nullable=False)
    loginAttempts = db.Column(db.Integer(), nullable=False, default=0)
