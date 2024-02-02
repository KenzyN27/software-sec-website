from flask import Flask


def create_app():
    app = Flask(__name__)
    # secret key to encrypt communication
    app.config['SECRET_KEY'] = "4ZqUkSkzQgdGTdqQtf1o73UqejhqTw6uu5mbaD7zkDE="

    # give app the Blueprints
    from .views import views
    from .auth import auth

    # prefix defines if it needs a prior address before accessing the defined route.
    # e.g. if url_prefix is /user/, the browser's address is www.123.com/user/<route>
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app