from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from os import environ
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    # secret key to encrypt communication

    # CHANGE HOW THE KEY IS IMPLEMENTED LATER
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
    db.init_app(app)

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
    # strong protection to keep session from being stolen
    login_manager.session_protection = 'strong'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app