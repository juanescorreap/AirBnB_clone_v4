#!/usr/bin/python3
"""
View for City objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def retrive_all_cities(state_id=None):
    """"Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state_cities = state.cities
    return jsonify([City.to_dict(city) for city in state_cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def retrive_city(city_id=None):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(City.to_dict(city))


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id=None):
    """" Deletes a City object and return an empty dict and 200 status"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_city(state_id=None):
    """" Creates a City object"""
    request_json = request.get_json()
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if request_json is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request_json:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    city = City(**request_json)
    city.state_id = state_id
    city.save()
    return make_response(jsonify(State.to_dict(city)), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id=None):
    """" Updates a City object"""
    request_json = request.get_json()
    if request_json is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in request_json.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    city.save()
    return make_response(jsonify(State.to_dict(city)), 200)
