#!/usr/bin/python3
"""
View for Place objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.city import City
from models.place import Place
from models.user import User
from models import storage


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def retrive_all_places(city_id=None):
    """"Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city_places = city.places
    return jsonify([Place.to_dict(place) for place in city_places]), 200


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def retrive_place(place_id=None):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(Place.to_dict(place)), 200


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id=None):
    """" Deletes a Place object and returns an
    empty dict and 200 as the status"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id=None):
    """" Creates a Place object"""
    request_json = request.get_json()
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if request_json is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in request_json:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = storage.get(User,  request_json.get('user_id'))
    if not user:
        abort(404)
    if 'name' not in request_json:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    place = Place(**request_json)
    place.city_id = city_id
    place.save()
    return make_response(jsonify(Place.to_dict(place)), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id=None):
    """" Updates a Place object"""
    request_json = request.get_json()
    if request_json is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in request_json.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return make_response(jsonify(Place.to_dict(place)), 200)
