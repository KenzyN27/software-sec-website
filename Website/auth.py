from flask import Blueprint

# setup Blueprint for authentication webpages
auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return "<p>Login</p>"

@auth.route('/logout')
def logout():
    return "<p>logout</p>"

@auth.route('/create-account')
def create_account():
    return "<p>create account</p>"