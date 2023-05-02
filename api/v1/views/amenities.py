#!/usr/bin/python3
"""This module contain API for model class Amenity"""
from models import storage
import uuid
from models.amenity import Amenity
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.get('/amenities', strict_slashes=False)
def get_amenities():
    """Retrieve all amenities in memory"""
    amenities = storage.all(Amenity)
    if not amenities:
        abort(404)
    amenities_list = [amenity.to_dict() for amenity in amenities.values()]
    return jsonify(amenities_list)


@app_views.get('/amenities/<string:amenity_id>',
               strict_slashes=False)
def get_amenity(amenity_id):
    """Get a Amenity given it's ID"""
    amenity = storage.get(Amenity, amenity_id)
    try:
        return jsonify(amenity.to_dict())
    except AttributeError:
        abort(404)


@app_views.delete('/amenities/<string:amenity_id>', strict_slashes=False)
def delete_Amenity(amenity_id):
    """Delete amenity from the the database"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.post('/amenities', strict_slashes=False)
def add_amenity():
    """Add a Amenity to a amenity where it belongs"""
    try:
        data = request.get_json()
        amenity = Amenity()
        amenity.id = data.get('id', str(uuid.uuid4()))
        amenity.name = data['name']
        amenity.save()
        return make_response(jsonify(amenity.to_dict()), 201)

    except KeyError:
        abort(400, "Missing name")
    except Exception:
        abort(400, "Not a JSON")


@app_views.put('/amenities/<string:amenity_id>', strict_slashes=False)
def update_amenity(amenity_id):
    """Update amenity with new input"""
    amenity = storage.get(Amenity, amenity_id)
    try:
        data = request.get_json()
        if data['name'] and type(data['name']) is str:
            amenity.name = data.get('name')
            amenity.save()
        return make_response(jsonify(amenity.to_dict()), 200)

    except KeyError:
        abort(400, "Missing name")
    except AttributeError:
        abort(404)
    except Exception:
        abort(400, "Not a JSON")