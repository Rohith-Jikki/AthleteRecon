from flask import Blueprint, render_template, redirect, session, request
from functools import wraps
from .models import User
from .__init__ import player_details, club_details

views = Blueprint("views", __name__)

# Decorators


def player(function):
    @wraps(function)
    def wrap(*args, **kwargs):
        if session['club_or_player'] == 'player':
            return function(*args, **kwargs)
        else:
            return redirect('/logout')
    return wrap


def club(function):
    @wraps(function)
    def wrap(*args, **kwargs):
        if session['club_or_player'] == 'club':
            return function(*args, **kwargs)
        else:
            return redirect('/logout')
    return wrap


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


# Player Pages

@views.route('/players', methods=['POST', 'GET'])
@login_required
@player
def player_page():
    playerDetails = player_details.find_one({'_id': session['user']['_id']})
    if request.method == 'POST':
        return User().update_profile(previous_data_identifier={
            '_id': session['user']['_id']}, database=player_details)
    return render_template('main.html', playerDetails=playerDetails)


@views.route('/career')
@login_required
@player
def career_page():
    return render_template("career.html")


@views.route('/player-profile', methods=['GET', 'POST'])
@login_required
@player
def player_profile_page():
    playerDetails = player_details.find_one({'_id': session['user']['_id']})
    return render_template("player-profile.html", player_details=playerDetails)


# Club pages

@views.route('/clubs')
@login_required
@club
def clubs_page():
    clubDetails = club_details.find_one({"_id": session['user']['_id']})
    return render_template("club-main.html", club_details=clubDetails)


@views.route('/edit-club-profile', methods=['GET', 'POST'])
@login_required
@club
def edit_club_details():
    return render_template("edit-club.html")
