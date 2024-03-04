from flask import Blueprint, render_template
from flask_login import login_required, current_user

# setup Blueprint for views not related to authentication
views = Blueprint('views', __name__)

# define homepage of website (i.e. the root)
@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/contact')
@login_required
def contact():
    return render_template("contact.html", user=current_user)

@views.route('/details')
@login_required
def account():
    return render_template("details.html", user=current_user)