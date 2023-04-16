from flask import Blueprint, render_template, redirect, session, request
from functools import wraps
from .models import *
from .__init__ import player_details, club_details, player_posts, player_posts_analysis
from .common_functions import *

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
            '_id': session['user']['_id']}, database=player_details, new_data={
            "$set": {
                "name": request.form.get('name'),
                "email": request.form.get('email'),
                "date-of-birth": request.form.get('date-of-birth'),
                "contact-number": request.form.get('phone'),
                # physical details
                "height": request.form.get('height'),
                "weight": request.form.get('weight'),
                "medical-conditions": null_or_value(request.form.get('medical-conditions'))
            }
        })
    return render_template('main.html', playerDetails=playerDetails)


@views.route('/career')
@login_required
@player
def career_page():
    posts = player_posts[session['user']['_id']]
    return render_template("career.html", posts=posts.find(), image_maker=image_maker)


@views.route('/player-profile', methods=['GET', 'POST'])
@login_required
@player
def player_profile_page():
    player_id = {'_id': session['user']['_id']}
    playerDetails = player_details.find_one(player_id)
    player_post_analysis_details = player_posts_analysis["a040eb1e56ff4cf8a26f641f8690d7e1"]
    data = {item['date']: item['post_count']
            for item in player_post_analysis_details.find()}
    return render_template("player-profile.html", player_details=playerDetails, data=data)


@views.route('/add-post', methods=['GET', 'POST'])
@login_required
@player
def add_post():
    if request.method == "POST":
        return Post().post(database=player_posts, analysis_database=player_posts_analysis)
    return render_template("add-post.html")


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
    if request.method == 'POST':
        return User().update_profile(database=club_details, previous_data_identifier={"_id": session['user']['_id']}, new_data={
            "$set": {
                "name": request.form.get('name'),
                "email": request.form.get('email'),
                "founder-name": request.form.get('founder-name'),
                "contact-number": request.form.get('phone'),
            }
        })
    return render_template("edit-club.html")


@views.route('/recruit', methods=['GET', 'POST'])
@login_required
@club
def recruit_players():
    return render_template("recruit.html", player_details=player_details.find(), calculateAge=calculateAge)
