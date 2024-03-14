from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from email_validator import validate_email, EmailNotValidError
from re import search
from flask_login import login_user, login_required, logout_user, current_user
from wtforms import Form, StringField, validators, PasswordField, DateTimeField
from flask_wtf import FlaskForm

# setup Blueprint for authentication webpages
auth = Blueprint('auth', __name__)

regex = '^(?=\S{8,30}$)(?=.+?\d)(?=.+?[a-z])(?=.+?[A-Z])(?=.+?[~!@#\$%\^&\*\(\)])'

# ^(?=\S{8,20}$) -> at start of the string, match at the end, check for length of 8-20 characters that are non-whitespace
# (?=.+?\d) -> look through string, check any character for one occurrence of a number
# (?=.+?[a-z]) -> look through string, check any character for one occurrence of a lowercase
# (?=.+?[A-Z]) -> look through string, check any character for one occurrence of a uppercase
# (?=.+?[~!@#\$%\^&\*\(\)]) -> look through string, check any character for one occurrence of given symbols

class CreateAccountForm(FlaskForm):
    email = StringField('email', validators=[validators.InputRequired(),validators.Length(min=4)],render_kw={'placeholder':"Enter Email"})
    name = StringField('name', validators=[validators.InputRequired(),validators.Length(min=4,max=320)],render_kw={'placeholder':"Enter Name"})
    dob = DateTimeField('dob', validators=[validators.InputRequired()], format='%Y-%m-%d')
    pswd1 = PasswordField('pswd1', validators=[validators.InputRequired(),validators.regexp(regex, message='Password must be secure. Requirements: A length of 8 to 20 characters, no spaces, and must contain at least one of each of the following: lowercase, uppercase, a number, and a symbol ( ~!@#$%^&*() )')],render_kw={'placeholder':"Enter Password"})
    pswd2 = PasswordField('pswd2', validators=[validators.InputRequired(),validators.Length(min=8, max=20),validators.EqualTo('pswd1', message='Passwords must match.')],render_kw={'placeholder':"Confirm Password"})

class LoginForm(FlaskForm):
    email = StringField('email', validators=[validators.InputRequired(),validators.Length(min=4)],render_kw={'placeholder':"Enter Email"})
    pswd = PasswordField('pswd', validators=[validators.InputRequired(),validators.Length(min=8,max=20)], render_kw={'placeholder':"Enter Password"})

class ChangePasswordForm(FlaskForm):
    pswd1 = PasswordField('pswd1', validators=[validators.InputRequired(),validators.regexp(regex, message='Password must be secure. Requirements: A length of 8 to 20 characters, no spaces, and must contain at least one of each of the following: lowercase, uppercase, a number, and a symbol ( ~!@#$%^&*() )')],render_kw={'placeholder':"Enter New Password"})
    pswd2 = PasswordField('pswd2', validators=[validators.InputRequired(),validators.Length(min=8, max=20),validators.EqualTo('pswd1', message='Passwords must match.')],render_kw={'placeholder':"Confirm New Password"})

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():

        usercheck = User.query.filter_by(email=form.email.data).first()

        if usercheck:
            if usercheck.loginAttempts >= 5:
                flash("User is locked out. Contact administration to fix.", category='error')
            elif check_password_hash(usercheck.password, form.pswd.data):
                flash("Logged in successfully!", category='success')
                login_user(usercheck)
                usercheck.loginAttempts = 0
                db.session.commit()
                return redirect(url_for('views.home'))
            else:
                attempts = 5 - usercheck.loginAttempts - 1
                if attempts > 0:
                    flash("Credentials given did not match our records. Try again.\nLogin attempts left: " + str(attempts), category='error')
                    usercheck.loginAttempts += 1
                    db.session.commit()
                else:
                    usercheck.loginAttempts += 1
                    db.session.commit()
                    flash("User has been locked out. Contact administration to fix.", category='error')
        else :
            flash("Given email does not have an account.", category='error')

    return render_template("login.html", user=current_user, form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/create_account', methods=['GET', 'POST'])
def create_account():
    form = CreateAccountForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        try:
            validate_email(form.email.data)
            # check if user exists w/ email already
            userresult = User.query.filter_by(email=form.email.data).first()

            if userresult:
                flash("User already exists.", category='error')
            else:
                if not search('\s', form.pswd1.data):
                    newUser = User(email = form.email.data, password = generate_password_hash(form.pswd1.data, method='pbkdf2', salt_length=16), name = form.name.data, dateOfBirth = form.dob.data)
                    db.session.add(newUser)
                    db.session.commit()

                    flash("Account created!", category='success')
                    return redirect(url_for('auth.login'))
                else:
                    flash('Password must be secure. Requirements: A length of 8 to 30 characters, no spaces, and must contain at least one of each of the following: lowercase, uppercase, a number, and a symbol ( ~!@#$%^&*() )', category='error')
        except EmailNotValidError:
            flash("Email must be a valid email.", category='error')

    return render_template("create_account.html", user=current_user, form=form)

@auth.route('change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        current_user.password = generate_password_hash(form.pswd1.data, method='pbkdf2', salt_length=16)
        db.commit()
        flash("Password changed!", category='success')
        return redirect(url_for('views.home'))
            
    return render_template("change_password.html", user=current_user, form=form)