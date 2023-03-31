import os
from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.environ.get("REF"))
db = client["user_login_system"]
users = db['clubs_credentials']


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('KEY')
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    return app
