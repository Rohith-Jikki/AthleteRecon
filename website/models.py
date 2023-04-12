from flask import jsonify, request, session, redirect
import uuid
from passlib.hash import pbkdf2_sha256


class User:
    def start_session(self, user, club_or_player):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        session['club_or_player'] = club_or_player
        return jsonify(user), 200

    def signup(self, name, email, password, database, details_database):
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
            if request.form.get('club-or-player') == 'player':
                player_details = {
                    "_id": self.id,
                    "name": request.form.get('name'),
                    "email": request.form.get('email'),
                    "date-of-birth": "null",
                    "contact-number": "null",
                    # physical details
                    "height": "null",
                    "weight": "null",
                    "medical-conditions": "null",
                }
                sport = request.form.get("sport-select")
                if sport == "football":
                    player_details["sport"] = sport
                    player_details["position"] = request.form.get(
                        'football-position')
                    player_details["strong_foot"] = request.form.get(
                        'strong-foot')
                else:
                    player_details['sport'] = sport
                    player_details['role'] = request.form.get('role')
                    player_details['play-style'] = request.form.get('style')
                details_database.insert_one(player_details)
                return self.start_session(user, club_or_player='player')
            else:
                club_details = {
                    "_id": self.id,
                    "name": request.form.get('name'),
                    "founder-name": "null",
                    "email": request.form.get('email'),
                    "contact-number": "null",
                    "sport": request.form.get('sport-select')
                }
                details_database.insert_one(club_details)
            return self.start_session(user, club_or_player='club')

        return jsonify({"error": "account cannot be created"}), 400

    def sign_out(self):
        session.clear()
        return redirect('/')

    def login(self, database, club_or_player):
        user = database.find_one({
            "email": request.form.get("emailInput")
        })
        if user and pbkdf2_sha256.verify(request.form.get("passwordInput"), user['password']):
            return self.start_session(user, club_or_player=club_or_player)
        return jsonify({"error": "Invalid login credentials"}), 401

    def update_profile(self, database, previous_data_identifier, new_data):
        if database.update_one(previous_data_identifier, new_data):
            return jsonify({"success": "Details Updated"}), 200
        return jsonify({"error": "Cannont Update Details"}), 400
