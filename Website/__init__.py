from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "4ZqUkSkzQgdGTdqQtf1o73UqejhqTw6uu5mbaD7zkDE="

    return app