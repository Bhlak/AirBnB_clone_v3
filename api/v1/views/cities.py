#!/usr/bin/python3
"""This module contain API for model class City"""
from models import storage
import uuid
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.get('/states/<string:state_id>/cities',
               strict_slashes=False)
def get_cities_by_state(state_id):
    """Get a all cities in a certain state"""
    state = storage.get(State, state_id)
    try:
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)
    except AttributeError:
        abort(404)


@app_views.get('/cities/<string:city_id>',
               strict_slashes=False)
def get_city(city_id):
    """Get a city given it's ID"""
    city = storage.get(City, city_id)
    try:
        return jsonify(city.to_dict())
    except AttributeError:
        abort(404)


@app_views.delete('/cities/<string:city_id>', strict_slashes=False)
def delete_city(city_id):
    """Delete city from the the database"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.post('/states/<string:state_id>/cities',
                strict_slashes=False)
def add_city(state_id):
    """Add a city to a state where it belongs"""
    state = storage.get(State, state_id)
    try:
        data = request.get_json()
        city = City()
        city.id = data.get('id', str(uuid.uuid4()))
        city.name = data['name']
        city.state_id = state.id
        city.save()
        return make_response(jsonify(city.to_dict()), 201)
    except KeyError:
        abort(400, "Missing name")
    except AttributeError:
        abort(404)
    except Exception:
        abort(400, "Not a JSON")


@app_views.put('/cities/<string:city_id>', strict_slashes=False)
def update_city(city_id):
    """Update city with new input"""
    city = storage.get(City, city_id)
    try:
        data = request.get_json()
        if data['name'] and type(data['name']) is str:
            city.name = data.get('name')
            city.save()
            return make_response(jsonify(city.to_dict()), 201)
    except KeyError:
        abort(400, "Missing name")
    except AttributeError:
        abort(404)
    except Exception:
        abort(400, "Not a JSON")