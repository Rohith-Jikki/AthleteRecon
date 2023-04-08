from flask import jsonify, request, session, redirect
import uuid
from passlib.hash import pbkdf2_sha256


class User:
    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
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
                    "date-of-birth": " ",
                    "contact-number": " ",
                    # physical details
                    "height": " ",
                    "weight": " ",
                    "medical-conditions": " ",
                }
                sport = request.form.get("sport-select")
                if sport == "football":
                    player_details["sport"] = sport
                    player_details["position"] = request.form.get(
                        'football-position')
                    player_details["strong_foot"] = request.form.get(
                        'strong-foot')
                details_database.insert_one(player_details)

            return self.start_session(user)

        return jsonify({"error": "account cannot be created"}), 400

    def sign_out(self):
        session.clear()
        return redirect('/')

    def login(self, database):
        user = database.find_one({
            "email": request.form.get("emailInput")
        })
        if user and pbkdf2_sha256.verify(request.form.get("passwordInput"), user['password']):
            return self.start_session(user)
        return jsonify({"error": "Invalid login credentials"}), 401
