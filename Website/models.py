from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    # have a separate ID as primary key instead of the email due to uniqueness/scecurity
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(50))
    name = db.Column(db.String(150))