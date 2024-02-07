from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

# setup Blueprint for authentication webpages
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return render_template("logout.html")

@auth.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        pswd1 = request.form.get('pswd1')
        pswd2 = request.form.get('pswd2')
        
        if len(email) < 4:
            flash("Email must be greater than 4 characters.", category='error')
        elif len(name) < 2:
            flash("First name must be greater than 1 character.", category='error')
        elif pswd1 != pswd2:
            flash("Passwords do not match.", category='error')
        elif len(pswd1) < 7:
            flash("Password must be secure. Requirements: At least 8 characters and can use lowercase, uppercase, or !@#$%^&()", category='error')
        else:
            new_user = User(email=email, password=generate_password_hash(pswd1, method='pbkdf2'), name=name)
            db.session.add(new_user)
            db.session.commit()
            flash("Account created!", category='success')
            # send user home
            return redirect(url_for('views.home'))
                   
    return render_template("create_account.html")