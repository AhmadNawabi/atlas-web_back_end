#!/usr/bin/env python3
"""
Module containing routes related to User operations.
Handles user retrieval, creation, update, and deletion.

This module assumes that `request.current_user` is
set in a `before_request` middleware in the main app file
when using BasicAuth or similar authentication methods.
"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """
    GET /api/v1/users
    Return:
        - List of all User objects in JSON format.
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """
    GET /api/v1/users/<user_id>
    Path parameter:
        - user_id: ID of the user to retrieve or 'me' for current user.
    Return:
        - JSON of User object.
        - 404 if User not found.
    """
    if user_id is None:
        abort(404)

    current_user = getattr(request, "current_user", None)

    if user_id == "me":
        if current_user is None:
            abort(404)
        return jsonify(current_user.to_json())

    user = User.get(user_id)
    if user is None:
        abort(404)

    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """
    DELETE /api/v1/users/<user_id>
    Path parameter:
        - user_id: ID of the user to delete.
    Return:
        - Empty JSON with status 200 if deleted.
        - 404 if User not found.
    """
    if user_id is None:
        abort(404)

    user = User.get(user_id)
    if user is None:
        abort(404)

    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """
    POST /api/v1/users
    JSON body:
        - email (required)
        - password (required)
        - first_name (optional)
        - last_name (optional)
    Return:
        - Created User JSON with status 201.
        - Error JSON with status 400 on failure.
    """
    try:
        rj = request.get_json()
    except Exception:
        rj = None

    error_msg = None
    if rj is None:
        error_msg = "Wrong format"
    elif rj.get("email", "") == "":
        error_msg = "email missing"
    elif rj.get("password", "") == "":
        error_msg = "password missing"

    if error_msg is None:
        try:
            user = User()
            user.email = rj.get("email")
            user.password = rj.get("password")
            user.first_name = rj.get("first_name")
            user.last_name = rj.get("last_name")
            user.save()
            return jsonify(user.to_json()), 201
        except Exception as e:
            error_msg = "Can't create User: {}".format(e)

    return jsonify({'error': error_msg}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """
    PUT /api/v1/users/<user_id>
    Path parameter:
        - user_id: ID of the user to update.
    JSON body:
        - first_name (optional)
        - last_name (optional)
    Return:
        - Updated User JSON with status 200.
        - Error JSON with status 400 on failure or 404 if not found.
    """
    if user_id is None:
        abort(404)

    user = User.get(user_id)
    if user is None:
        abort(404)

    try:
        rj = request.get_json()
    except Exception:
        rj = None

    if rj is None:
        return jsonify({'error': "Wrong format"}), 400

    if rj.get('first_name') is not None:
        user.first_name = rj.get('first_name')
    if rj.get('last_name') is not None:
        user.last_name = rj.get('last_name')

    user.save()
    return jsonify(user.to_json()), 200
