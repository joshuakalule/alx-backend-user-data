#!/usr/bin/env python3
"""Basic Flask app."""

from auth import Auth
from flask import abort, Flask, jsonify, request

AUTH = Auth()
app = Flask(__name__)


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """End point for loging in"""

    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        abort(401)

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)

    payload = {
        'email': email,
        "message": "logged in"
    }
    response = jsonify(payload)
    response.set_cookie('session_id', session_id)
    return response, 200


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
    """End point to register a user."""
    content_type = request.content_type
    if content_type == 'application/json':
        data = request.get_json(silent=True)
    else:
        data = request.form

    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"message": "expected email and password"}), 400

    email = data.get('email')
    password = data.get('password')

    try:
        user = AUTH.register_user(email=email, password=password)
    except ValueError:
        # user already exists
        return jsonify({"message": "email already registered"}), 400

    json_output = {
     "email": user.email,
     "message": "user created"
    }

    return jsonify(json_output), 200


@app.route('/', methods=['GET'])
def home():
    """Home end point."""
    return jsonify({"message": "Bienvenue"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
