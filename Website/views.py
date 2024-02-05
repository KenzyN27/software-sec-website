from flask import Blueprint, render_template

# setup Blueprint for views not related to authentication
views = Blueprint('views', __name__)

# define homepage of website (i.e. the root)
@views.route('/')
def home():
    return render_template("home.html")

