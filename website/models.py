from base64 import b64encode
from flask import jsonify, request, session, redirect
import uuid
from passlib.hash import pbkdf2_sha256


class User:
    def __init__(self):
        self.profile_image = None
        self.id = None

    def start_session(self, user, club_or_player):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        session['club_or_player'] = club_or_player
        return jsonify(user), 200

    def signup(self, name, email, password, database, details_database, analysis_database):
        self.id = uuid.uuid4().hex
        user = {
            "_id": self.id,
            "name": request.form.get(name),
            "email": request.form.get(email),
            "password": request.form.get(password)
        }

        # Encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        if database.find_one({'email': user["email"]}):
            return jsonify({"error": "email address already in use"}), 400

        # Insert into the Database
        if database.insert_one(user):
            profile_picture = request.files['picture'].read()
            self.profile_image = b64encode(profile_picture)
            profile_image_type = request.files['picture'].content_type
            if request.form.get('club-or-player') == 'player':

                player_details = {
                    "_id": self.id,
                    "name": request.form.get('name'),
                    "email": request.form.get('email'),
                    "date-of-birth": "null",
                    "contact-number": "null",
                    "profile-picture": self.profile_image,
                    "profile-picture-type": profile_image_type,
                    # physical details
                    "gender": request.form.get('gender'),
                    "height": "null",
                    "weight": "null",
                    "medical-conditions": "null",
                }
                player_analysis_details = {
                    'performance': 'no'
                }
                sport = request.form.get("sport-select")
                match request.form.get("sport-select"):
                    case 'football':
                        sport_details = {
                            'sport': sport,
                            'position': request.form.get('football-position'),
                            'strong_foot': request.form.get('strong-foot')
                        }
                        player_details.update(sport_details)
                        player_analysis_details.update(sport_details)
                    case 'cricket':
                        cricket_details = {
                            'sport': sport,
                            'role': request.form.get('role'),
                            'play-style': request.form.get('style')
                        }
                        player_details.update(cricket_details)
                        player_analysis_details.update(cricket_details)
                details_database.insert_one(player_details)
                analysis_location = analysis_database[self.id]
                analysis_location.insert_one(player_analysis_details)
                return self.start_session(user, club_or_player='player')
            else:
                club_details = {
                    "_id": self.id,
                    "name": request.form.get('name'),
                    "founder-name": "null",
                    "email": request.form.get('email'),
                    "contact-number": "null",
                    "sport": request.form.get('sport-select'),
                    "profile-picture": self.profile_image,
                    "profile-picture-type": profile_image_type
                }
                details_database.insert_one(club_details)
            return self.start_session(user, club_or_player='club')

        return jsonify({"error": "account cannot be created"}), 400

    def sign_out(self):
        session.clear()
        return redirect('/')

    def login(self, database, club_or_player):
        user = database.find_one({"email": request.form.get("emailInput")})
        if user and pbkdf2_sha256.verify(request.form.get("passwordInput"), user['password']):
            return self.start_session(user, club_or_player=club_or_player)
        return jsonify({"error": "Invalid login credentials"}), 401

    def update_profile(self, database, previous_data_identifier, new_data):
        if database.update_one(previous_data_identifier, new_data):
            return jsonify({"success": "Details Updated"}), 200
        return jsonify({"error": "Cannot Update Details"}), 400

    def post(self, database):
        image = request.files['certificate'].read()
        image_b64 = b64encode(image)
        document = {
            "_id": uuid.uuid4().hex,
            "title": request.form.get('title'),
            "image": image_b64,
            "description": request.form.get('post-description'),
            "content-type": request.files['certificate'].content_type,
            "date": request.form.get('date')
        }
        post_location = database[session['user']['_id']]
        if post_location.insert_one(document):
            return redirect('/career')
        return jsonify({"error": "Cannot Post"}), 500


class Post:
    @staticmethod
    def add_post_analysis(self, date, post_id, database) -> bool:
        # Check if the date already exists in the database
        post = database.find_one({'date': date})
        if post is None:
            if database.insert_one(
                    {'date': date, 'post_count': 1, 'posts': [post_id]}):
                return True
        else:
            return True if database.update_one({'date': date},
                                               {'$inc': {'post_count': 1},
                                                '$push': {'posts': post_id}}
                                               ) else False
        return False

    def post(self, database, analysis_database):
        image = request.files['certificate'].read()
        date = request.form.get('date')
        post_id = uuid.uuid4().hex
        player_id = session['user']['_id']
        image_b64 = b64encode(image)
        document = {
            "_id": post_id,
            "title": request.form.get('title'),
            "image": image_b64,
            "description": request.form.get('post-description'),
            "content-type": request.files['certificate'].content_type,
            "date": date
        }
        post_location = database[player_id]
        analysis_database_location = analysis_database[player_id]
        if post_location.insert_one(document):
            if self.add_post_analysis(date=date[:7], post_id=post_id, database=analysis_database_location):
                return redirect('/career')
        return jsonify({"error": "Cannot Post"}), 500


class Club:
    @staticmethod
    def send_message(club_database,
                     player_database,
                     message: str,
                     player_inbox_message: str) -> object:
        if club_database.insert_one(message):
            if player_database.insert_one(player_inbox_message):
                print('done')
                return redirect('/outbox')
        return jsonify({"error": "cannot be sent"}), 400
