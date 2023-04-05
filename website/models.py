from flask import jsonify, request, session, redirect
import uuid
from passlib.hash import pbkdf2_sha256
from .__init__ import users


class User:
    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200

    def signup(self, name, email, password):
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get(name),
            "email": request.form.get(email),
            "password": request.form.get(password)
        }

        # Encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        if users.find_one({'email': user["email"]}):
            return jsonify({"error": "email address already in use"}), 400

        # Insert into the Database
        if users.insert_one(user):
            return self.start_session(user)

        return jsonify({"error": "account cannot be created"}), 400

    def sign_out(self):
        session.clear()
        return redirect('/')

    def login(self):
        user = users.find_one({
            "email": request.form.get("emailInput")
        })
        if user and pbkdf2_sha256.verify(request.form.get("passwordInput"), user['password']):
            return self.start_session(user)
        return jsonify({"error": "Invalid login credentials"}), 401
