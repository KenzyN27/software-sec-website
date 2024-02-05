from flask import Blueprint, render_template

# setup Blueprint for authentication webpages
auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return render_template("logout.html")

@auth.route('/create-account')
def create_account():
    return render_template("create_account.html")