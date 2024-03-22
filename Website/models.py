from . import db, app
from flask_login import UserMixin
import jwt
from time import time
from os import environ
from itsdangerous import URLSafeTimedSerializer as Serializer

class User(db.Model, UserMixin):
    # have a separate ID as primary key instead of the email due to uniqueness/security
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(320), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(71), nullable=False)
    dateOfBirth = db.Column(db.Date)
    loginAttempts = db.Column(db.Integer(), nullable=False, default=0)
    isAdmin = db.Column(db.Boolean, nullable=False, default=False)

    def get_reset_token(self):
        serial = Serializer(app.config.get('SECRET_KEY'))
        return serial.dumps([self.email])
    
    def verify_token(token):
        serial=Serializer(app.config.get('SECRET_KEY'))
        try:
            data = serial.loads(token)
            email = data[0]
        except:
            return None
        return User.query.filter_by(email=email).first()