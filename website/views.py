from functools import wraps

import pymongo
from flask import Blueprint, render_template

from .__init__ import *
from .common_functions import *
from .models import *

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
                "profile-picture": b64encode(request.files['picture'].read()),
                "profile-picture-type": request.files['picture'].content_type,

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
    playerDetails = player_details.find_one(
        player_id, {"profile-picture": 0, "profile-picture-type": 0})
    pictureDetails = player_details.find_one(
        player_id, {"profile-picture": 1, "profile-picture-type": 1})
    player_post_analysis_details = player_posts_analysis[player_id['_id']]
    data = {item['date']: item['post_count']
            for item in player_post_analysis_details.find()}
    return render_template("player-profile.html",
                           player_details=playerDetails,
                           data=data,
                           pictureDetails=pictureDetails,
                           image_maker=image_maker)


@views.route('/add-post', methods=['GET', 'POST'])
@login_required
@player
def add_post():
    if request.method == "POST":
        return Post().post(database=player_posts, analysis_database=player_posts_analysis)
    return render_template("add-post.html")


@views.route('/inbox')
@login_required
@player
def inbox():
    inbox_messages = player_inbox[session['user']['_id']]
    return render_template("inbox.html", inbox_messages=inbox_messages.find())


@views.route('/performance')
@login_required
@player
def performance():
    values = data_analysis[session['user']['_id']].find_one()
    if values['performance'] == 'yes':
        match values['sport']:
            case 'cricket':
                match values['role']:
                    case 'Batsman':
                        return render_template('batsman.html', values=values)
                    case 'bowler':
                        pass
                    case 'all-rounder':
                        pass
                    case _:
                        return render_template('buy-performance.html')
            case 'football':
                match values['football-position']:
                    case 'attacker':
                        pass
                    case 'mid-fielder':
                        pass
                    case 'defender':
                        pass
                    case 'goal-keeper':
                        pass
                    case _:
                        return render_template('buy-performance.html')
        return render_template('performance.html')
    return render_template('buy-performance.html')


# Club pages


@views.route('/clubs')
@login_required
@club
def clubs_page():
    clubDetails = club_details.find_one({"_id": session['user']['_id']}, {
        "profile-picture": 0, "profile-picture-type": 0})
    pictureDetails = club_details.find_one({"_id": session['user']['_id']}, {
        "profile-picture": 1, "profile-picture-type": 1})
    return render_template("club-main.html", club_details=clubDetails,
                           pictureDetails=pictureDetails,
                           image_maker=image_maker)


@views.route('/edit-club-profile', methods=['GET', 'POST'])
@login_required
@club
def edit_club_details():
    clubDetails = club_details.find_one({'_id': session['user']['_id']})
    if request.method == 'POST':
        return User().update_profile(database=club_details,
                                     previous_data_identifier={"_id": session['user']['_id']},
                                     new_data={
                                         "$set": {
                                             "name": request.form.get('name'),
                                             "email": request.form.get('email'),
                                             "founder-name": request.form.get('founder-name'),
                                             "contact-number": request.form.get('phone'),
                                             "profile-picture": b64encode(request.files['picture'].read()),
                                             "profile-picture-type": request.files['picture'].content_type
                                         }
                                     })
    return render_template("edit-club.html", club_details=clubDetails)


@views.route('/recruit', methods=['GET', 'POST'])
@login_required
@club
def recruit_players():
    player_data = player_details.find()
    if request.method == "POST":
        if 'player_profile_button' in request.form:
            session['player_id'] = request.form.get('player_profile_button')
            return redirect('/player-recruit-profile')
        elif 'sort_button' in request.form:
            filter_type = request.form.get("filter")
            match request.form.get("sort"):
                case 'weight_hl':
                    player_data = player_details.find({"sport": filter_type}).sort('weight', pymongo.DESCENDING)
                case 'weight_lh':
                    player_data = player_details.find({"sport": filter_type}).sort('weight', pymongo.ASCENDING)
                case 'height_hl':
                    player_data = player_details.find({"sport": filter_type}).sort('height', pymongo.DESCENDING)
                case 'height_lh':
                    player_data = player_details.find({"sport": filter_type}).sort('height', pymongo.ASCENDING)
                case 'age_hl':
                    player_data = player_details.find({"sport": filter_type}).sort('date-of-birth', pymongo.DESCENDING)
                case 'age_lh':
                    player_data = player_details.find({"sport": filter_type}).sort('date-of-birth', pymongo.ASCENDING)
            return render_template("recruit.html",
                                   player_details=player_data,
                                   calculateAge=calculateAge,
                                   )
    return render_template("recruit.html", player_details=player_data, calculateAge=calculateAge)


@views.route('/player-recruit-profile', methods=['GET', 'POST'])
@login_required
@club
def player_recruit_profile():
    # Database Referrals

    player_id = session['player_id']
    playerDetails = player_details.find_one(
        player_id, {"profile-picture": 0, "profile-picture-type": 0})
    pictureDetails = player_details.find_one(
        player_id, {"profile-picture": 1, "profile-picture-type": 1})
    player_post_analysis_details = player_posts_analysis[player_id]
    data = {item['date']: item['post_count']
            for item in player_post_analysis_details.find()}
    posts = player_posts[player_id]

    if request.method == 'POST':
        club_id = session['user']["_id"]
        code = referral_code_generator(name=club_id)
        Club().send_message(club_database=club_outbox[club_id],
                            message=inbox_message(
                                name='player-id',
                                Id=request.form.get("player_id"),
                                description=request.form.get('message'),
                                code=code,

                            ),
                            player_inbox_message=inbox_message(
                                name='club-id',
                                Id=club_id,
                                description=request.form.get('message'),
                                code=code
                            ),
                            player_database=player_inbox[request.form.get('player_id')]
                            )
    return render_template("recruit-profile.html",
                           player_details=playerDetails,
                           player_post_analysis_details=player_post_analysis_details,
                           data=data,
                           posts=posts.find(),
                           image_maker=image_maker,
                           pictureDetails=pictureDetails)


@views.route('/outbox', methods=['GET', 'POST'])
@login_required
@club
def outbox():
    messages = club_outbox[session['user']['_id']]
    return render_template('outbox.html', messages=messages.find())
