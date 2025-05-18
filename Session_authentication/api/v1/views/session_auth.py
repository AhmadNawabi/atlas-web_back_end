#!/usr/bin/env python3
"""Session authentication views"""
from flask import request, jsonify, make_response
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """Handles the session authentication login"""

    # Retrieve form data
    email = request.form.get('email')
    password = request.form.get('password')

    # Check for missing email
    if not email:
        return jsonify({"error": "email missing"}), 400

    # Check for missing password
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Find user by email
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    # Validate password
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Avoid circular import by importing here
    from api.v1.app import auth

    # Create session
    session_id = auth.create_session(user.id)
    response = make_response(jsonify(user.to_json()))

    # Set cookie with session ID
    session_name = getenv("SESSION_NAME")
    response.set_cookie(session_name, session_id)

    return response
