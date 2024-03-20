from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman
import os
from os import environ
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

talisman = Talisman()

csp = {
    'default-src': '\'self\'',
    'object-src': '\'none\'',
}

def create_app():
    app = Flask(__name__)
    # secret key to encrypt communication

    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
    db.init_app(app)
    bcrypt.init_app(app)
    talisman.init_app(app, content_security_policy=csp, x_xss_protection = True, session_cookie_secure = True)

    # give app the Blueprints
    from .views import views
    from .auth import auth

    # prefix defines if it needs a prior address before accessing the defined route.
    # e.g. if url_prefix is /user/, the browser's address is www.123.com/user/<route>
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # import the database defines first before creating database
    from .models import User

    # SQLAlchemy was updated to automatically not replace db if already there. Created as follows:
    with app.app_context():
        db.create_all()

    # CSRF define
    csrf = CSRFProtect()
    csrf.init_app(app)

    # login manager defined
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = ''
    # strong protection to keep session from being stolen
    login_manager.session_protection = 'strong'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app