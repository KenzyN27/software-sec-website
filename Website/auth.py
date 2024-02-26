from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from sqlalchemy.sql import text

# setup Blueprint for authentication webpages
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pswd')

        #usercheck = User.query.filter_by(email=email).first()

        usercheck = db.session.execute(text("SELECT * FROM Users WHERE email = :e"), {'e': email}).fetchone()

        #if usercheck:
        if usercheck:
            if check_password_hash(usercheck[2], password):
                flash("Logged in successfully!", category='success')
                return redirect('views.home')
            else:
                flash("Credentials given did not match our records. Try again.", category='error')
            #print(usercheck[2])
        else :
            flash("Email given does not have an account.", category='error')


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

            # check if user exists w/ email already
            userresult = User.query.filter_by(email=email).first()

            if userresult:
                flash("User already exists.", category='error')
            else:
                #newUser = User(email = email, password = generate_password_hash(pswd1, method='pbkdf2'), name = name)
                #db.session.add(newUser)
                #db.session.commit()
                #flash("Account created!", category='success')
                # send user home
                #return redirect(url_for('auth.login'))

                addresult = db.session.execute(text("INSERT INTO Users (email, password, name) VALUES (:e, :p, :n)"), {'e': email, 'p': generate_password_hash(pswd1, method='pbkdf2'), 'n': name})
                db.session.commit()
                if addresult.rowcount == 1:
                    flash("Account created!", category='success')
                    return redirect(url_for('auth.login'))
                   
    return render_template("create_account.html")