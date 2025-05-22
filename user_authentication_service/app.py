#!/usr/bin/env python3
"""
Flask application providing user authentication API endpoints.

Endpoints:
- /users          [POST]    Register a new user
- /sessions       [POST]    User login
- /sessions       [DELETE]  User logout
- /profile        [GET]     Retrieve user profile
- /reset_password [POST]    Generate reset password token
- /reset_password [PUT]     Update user password using reset token
"""

from typing import Any
from flask import Flask, request, jsonify, abort, redirect
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> Any:
    """Handle POST request for user registration.

    Returns:
        JSON response with email and message if successful,
        or 400 if email is already registered or missing fields.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(400)  # Bad request if email or password missing

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> Any:
    """Handle POST request for user login.

    Returns:
        JSON response with email and message if login successful,
        sets a session cookie.
        Aborts with 401 if credentials are missing or invalid.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(401)  # Unauthorized if email or password missing

    if not AUTH.valid_login(email, password):
        abort(401)  # Unauthorized if invalid login

    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)

    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> Any:
    """Log out a user by destroying their session.

    Returns:
        Redirects to home page on success.
        Aborts with 403 if session is missing or invalid.
    """
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)  # Forbidden if session ID is not present

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)  # Forbidden if no user found with the session ID

    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> Any:
    """GET /profile route to retrieve user profile.

    Returns:
        JSON response with user's email if authenticated,
        or 403 if unauthorized.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)  # Forbidden if session ID is invalid or user does not exist

    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> Any:
    """Handle POST request to generate a reset password token for a user.

    Returns:
        JSON response with email and reset token if successful,
        or 400 if email is missing,
        or 403 if user not found.
    """
    email = request.form.get('email')
    if not email:
        abort(400)  # Bad request if email is missing

    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)  # Forbidden if user does not exist


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> Any:
    """Handle PUT request to update a user's password.

    Returns:
        JSON response confirming password update if successful,
        or 400 if required fields are missing,
        or 403 if reset token is invalid.
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    if not email or not reset_token or not new_password:
        abort(400)  # Bad request if any field is missing

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)  # Forbidden if the reset token is invalid


if __name__ == "__main__":
    """
    Run the Flask development server on 0.0.0.0:5000.
    """
    app.run(host="0.0.0.0", port="5000")
