from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required, current_user
from wtforms import Form, StringField, validators
from flask_wtf import FlaskForm
from .models import User

# setup Blueprint for views not related to authentication
views = Blueprint('views', __name__)

contact_title = ""

class ContactForm(FlaskForm):
    title = StringField('title', validators=[validators.InputRequired(),validators.Length(min=4,max=100)])
    content = StringField('content', validators=[validators.InputRequired(),validators.Length(min=4,max=1000)])

# define homepage of website (i.e. the root)
@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    form = ContactForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        session['title'] = form.title.data
        print(form.title.data)
        return redirect(url_for('views.contact_submit'))
    return render_template("contact.html", user=current_user, form=form)

@views.route('/details')
@login_required
def account():
    return render_template("details.html", user=current_user)

@views.route('/contact_submit')
@login_required
def contact_submit():
    return render_template("submit.html", user=current_user, title=session['title'])

@views.route('/user_list')
@login_required
def user_list():
    if current_user.isAdmin == 1:
        print("Is admin")
        users = User.query.all()
        return render_template("userlist.html", users=users, user=current_user)
    else:
        print("Not admin")
        return redirect(url_for('views.home'), user=current_user)