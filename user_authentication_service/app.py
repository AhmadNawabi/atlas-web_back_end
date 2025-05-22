#!/usr/bin/env python3
from flask import Flask, request, jsonify, abort, redirect
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """Handle POST request for user registration"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(400)  # Bad request if email or password missing

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:  # User already exists
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """Handle POST request for user login"""
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
def logout():
    """Logs out a user by destroying their session."""
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)  # Forbidden if session ID is not present

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)  # Forbidden if no user found with the session ID

    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """GET /profile route to retrieve user profile."""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)  # Forbidden if session ID is invalid or user does not exist

    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """
    Handle POST request to generate a reset password token for a user.
    The user's email is obtained from the form data.
    Returns a JSON response with the email and reset token,
    or a 403 error if user not found.
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
def update_password():
    """
    Handle PUT request to update a user's password.
    Requires email, reset token, and new password fields in the form data.
    Returns a JSON response confirming password update,
    or a 403 error if reset token is invalid.
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
    app.run(host="0.0.0.0", port="5000")
