#!/usr/bin/env python3
""" Module of Session Auth views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """Register user session."""
    email = request.form.get('email', None)
    password = request.form.get('password', None)

    if not email or len(email) == 0:
        return jsonify({"error": "email missing"}), 400

    if not password or len(password) == 0:
        return jsonify({"error": "password missing"}), 400

    try:
        found_users = User.search({'email': email})
        if not found_users:
            raise Exception()
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    user = None
    for found_user in found_users:
        if found_user.is_valid_password(password):
            user = found_user
            break
    if not user:
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)

    response = jsonify(user.to_json())

    cookie_key = os.getenv('SESSION_NAME')
    cookie_value = str(session_id)
    response.set_cookie(cookie_key, cookie_value)

    return response, 200
