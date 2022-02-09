#!/usr/bin/python3
"""
View for Amenity objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def retrive_amenities(amenity_id=None):
    """" Retrives an Amenity object and returns a Json"""
    if amenity_id is None:
        amenities = storage.all('Amenity').values()
        return jsonify([Amenity.to_dict(amenity) for amenity in amenities])
    else:
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)
        return jsonify(Amenity.to_dict(amenity))


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id=None):
    """" Deletes an Amenity object and returns an empty dict and 200 status"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """" Creates an Amenity object"""
    request_json = request.get_json()
    if request_json is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request_json:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    amenity = Amenity(**request_json)
    amenity.save()
    return make_response(jsonify(Amenity.to_dict(amenity)), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id=None):
    """" Updates an Amenity object"""
    request_json = request.get_json()
    if request_json is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in request_json.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)
    amenity.save()
    return make_response(jsonify(Amenity.to_dict(amenity)), 200)
