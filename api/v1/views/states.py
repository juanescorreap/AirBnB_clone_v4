#!/usr/bin/python3
"""
View for State objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def retrive_states(state_id=None):
    """" Retrives a state object and returns a Json"""
    if state_id is None:
        states = storage.all('State').values()
        return jsonify([State.to_dict(state) for state in states])
    else:
        states = storage.get(State, state_id)
        if not states:
            abort(404)
        return jsonify(State.to_dict(states))


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id=None):
    """" Deletes a State object and return an empty dict and 200 status"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_states():
    """" Creates a State object"""
    request_json = request.get_json()
    if request_json is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request_json:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    state = State(**request_json)
    state.save()
    return make_response(jsonify(State.to_dict(state)), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_states(state_id=None):
    """" Updates a State object"""
    request_json = request.get_json()
    if request_json is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in request_json.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    state.save()
    return make_response(jsonify(State.to_dict(state)), 200)
