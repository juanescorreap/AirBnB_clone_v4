#!/usr/bin/python3
"""
View for User objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@app_views.route('/users', methods=['GET'], strict_slashes=False)
def retrive_users(user_id=None):
    """" Retrives a User object and returns a Json"""
    if user_id is None:
        users = storage.all('User').values()
        return jsonify([User.to_dict(user) for user in users])
    else:
        users = storage.get(User, user_id)
        if not users:
            abort(404)
        return jsonify(User.to_dict(users))


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id=None):
    """" Deletes a User object and returns an empty dict and 200 status"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """" Creates a User object"""
    request_json = request.get_json()
    if request_json is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in request_json:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    if 'password' not in request_json:
        return make_response(jsonify({'error': 'Missing password'}), 400)
    user = User(**request_json)
    user.save()
    return make_response(jsonify(User.to_dict(user)), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id=None):
    """" Updates a User object"""
    request_json = request.get_json()
    if request_json is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in request_json.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    user.save()
    return make_response(jsonify(User.to_dict(user)), 200)
