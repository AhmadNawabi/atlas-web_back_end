#!/usr/bin/env python3
"""Session authentication views.
This module provides a route for handling login via session-based
authentication, using email and password credentials submitted via POST.
"""
from flask import request, jsonify, make_response
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """POST /auth_session/login
    Handles login and session creation for users using email and password.

    Returns:
        - JSON error message with appropriate status code if login fails.
        - JSON representation of user and session cookie on success.
    """

    # Retrieve email and password from request form
    email = request.form.get('email')
    password = request.form.get('password')

    # Validate presence of email
    if not email:
        return jsonify({"error": "email missing"}), 400

    # Validate presence of password
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Attempt to find a user with the given email
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

    # Import auth object here to avoid circular import
    from api.v1.app import auth

    # Create session ID for the user
    session_id = auth.create_session(user.id)

    # Prepare JSON response with user data
    response = make_response(jsonify(user.to_json()))

    # Set session ID in cookie using env var SESSION_NAME
    session_name = getenv("SESSION_NAME")
    response.set_cookie(session_name, session_id)

    return response
