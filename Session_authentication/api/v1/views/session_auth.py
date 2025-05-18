#!/usr/bin/env python3
"""Session authentication views for login endpoint."""

from flask import request, jsonify, make_response
from models.user import User
from os import getenv


def session_login():
    """POST /auth_session/login
    Handles login and session creation for users using email and password.

    Returns:
        - 400 if email or password is missing
        - 404 if no user is found for the email
        - 401 if the password is incorrect
        - 200 with user JSON and session cookie on success
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth  # Delayed import to avoid circular import
    session_id = auth.create_session(user.id)
    response = make_response(jsonify(user.to_json()))
    session_name = getenv("SESSION_NAME")

    response.set_cookie(session_name, session_id)
    return response


# Register the route here to avoid circular imports at the top
from api.v1.views import app_views
app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)(session_login)
