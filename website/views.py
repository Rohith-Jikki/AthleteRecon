from flask import Blueprint, render_template, redirect, session
from functools import wraps
from .__init__ import player_details

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


@views.route('/career')
@login_required
def career_page():
    return render_template("career.html")


@views.route('/clubs')
def clubs_page():
    return render_template("club-main.html")


@views.route('/player-profile')
@login_required
def player_profile_page():
    playerDetails = player_details.find_one({'_id': session['user']['_id']})
    return render_template("player-profile.html", player_details=playerDetails)
