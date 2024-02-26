from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    # have a separate ID as primary key instead of the email due to uniqueness/scecurity
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(150), nullable=False)

    # FOR DEBUG, REMOVE LATER
    def __repr__(self):
        return f'<User {self.name}>'