from os import environ
from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


# DATABASE
client = MongoClient(environ.get("REF"))
db = client["user_login_system"]
db_two = client["user_details"]
player_posts = client["player_posts"]

users = db['players_credentials']
player_details = db_two['player_details']

club_users = db['clubs_credentials']
club_details = db_two['club_details']


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = environ.get('KEY')
    app.secret_key = environ.get("KEY")
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    return app
