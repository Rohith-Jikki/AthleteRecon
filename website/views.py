from flask import Blueprint, render_template, redirect, session
from functools import wraps

views = Blueprint("views", __name__)


# Decorators
def login_required(function):
    @wraps(function)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return function(*args, **kwargs)
        else:
            return redirect('/login')

    return wrap


@views.route('/')
def home():
    return render_template("home.html")


@views.route('/players')
@login_required
def player_page():
    return render_template('main.html')
