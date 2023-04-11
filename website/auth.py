from flask import Blueprint, render_template, request, flash
from .models import User
from .__init__ import users, club_users, player_details, club_details

auth = Blueprint("auth", __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if (str(request.form.get('club-or-player')) == 'player'):
            return User().login(database=users, club_or_player='player')
        else:
            return User().login(database=club_users, club_or_player='club')
    return render_template("login.html")


@auth.route('/logout')
def logout():
    return User().sign_out()


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        if len(name) < 2:
            flash(message="Name is too short", category='error')
        elif len(email) < 4:
            flash(message="email is too short", category='error')
        elif len(password) < 7:
            flash(message="password is less than 8 characters", category='error')
        else:
            if (str(request.form.get('club-or-player')) == 'player'):
                return User().signup(name='name', email='email', password="password", database=users, details_database=player_details)
            else:
                return User().signup(name='name', email='email', password="password", database=club_users, details_database=club_details)

    return render_template("signup.html")
