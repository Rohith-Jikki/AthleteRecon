from flask import Blueprint, render_template, request, flash
from .models import User


auth = Blueprint("auth", __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        return User().login()
    return render_template("login.html")


@auth.route('/logout')
def logout():
    return User().sign_out()


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST' and request.form.get("player") == 'player':
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
            return User().signup(name='name', email='email', password="password")

    return render_template("signup.html")
