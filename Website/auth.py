from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from email_validator import validate_email, EmailNotValidError
from re import search
from flask_login import login_user, login_required, logout_user, current_user
from wtforms import Form, StringField, validators, PasswordField

# setup Blueprint for authentication webpages
auth = Blueprint('auth', __name__)

regex = '^(?=\S{8,20}$)(?=.+?\d)(?=.+?[a-z])(?=.+?[A-Z])(?=.+?[~!@#\$%\^&\*\(\)])'

# ^(?=\S{8,20}$) -> at start of the string, match at the end, check for length of 8-20 characters that are non-whitespace
# (?=.+?\d) -> look through string, check any character for one occurrence of a number
# (?=.+?[a-z]) -> look through string, check any character for one occurrence of a lowercase
# (?=.+?[A-Z]) -> look through string, check any character for one occurrence of a uppercase
# (?=.+?[~!@#\$%\^&\*\(\)]) -> look through string, check any character for one occurrence of given symbols

def validatePassword(pswd1, pswd2):
    if pswd1 == pswd2:
        # if lowercase, uppercase, number, and symbol exists with no whitespace
        if search(regex, str(pswd1)) and not search('\s', str(pswd1)):
            return True
    flash("Password must be secure. Requirements: A length of 8 to 20 characters, no spaces, and must contain at least one of each of the following: lowercase, uppercase, a number, and a symbol ( ~!@#$%^&*() )", category='error')
    return False

class CreateAccountForm(Form):
    email = StringField('email', validators=[validators.InputRequired()])
    name = StringField('name', validators=[validators.InputRequired(),validators.Length(min=4,max=320)])
    pswd1 = PasswordField('pswd1')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        pswd = request.form.get('pswd')
        isRemembered = request.form.get('remember')

        usercheck = User.query.filter_by(email=email).first()

        #if usercheck:
        if usercheck:
            if check_password_hash(usercheck.password, pswd):
                flash("Logged in successfully!", category='success')
                if isRemembered:
                    login_user(usercheck, remember=True)
                else:
                    login_user(usercheck, remember=False)
                return redirect(url_for('views.home'))
            else:
                flash("Credentials given did not match our records. Try again.", category='error')
        else :
            flash("Given email does not have an account.", category='error')


    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        form = CreateAccountForm(request.form)
        
                   
    return render_template("create_account.html", user=current_user)

@auth.route('change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        pswd1 = request.form.get('pswd1')
        pswd2 = request.form.get('pswd2')

        if validatePassword(pswd1, pswd2):
            email = current_user.email
            print(email)
            flash("Password changed!", category='success')
            return redirect(url_for('views.home'))
            
    return render_template("change_password.html", user=current_user)