#!/usr/bin/python3
"""
Create a new view for Amenities objects
that handles all default RESTFul API actions
"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route("/amenities",
                 methods=["GET"],
                 strict_slashes=False)
def get_Amenities():
    """ list all amenities """
    get_amenities = storage.all("Amenity").values()
    list_amenities = []
    for element in get_amenities:
        list_amenities.append(element.to_dict())
    return jsonify(list_amenities)


@app_views.route("/amenities/<amenity_id>",
                 methods=["GET", "DELETE"],
                 strict_slashes=False)
def id_amenity(amenity_id):
    """ return id delete"""
    dict_amenity = storage.all("Amenity")
    list_amenities = []
    for element in dict_amenity:
        val = dict_amenity[element].to_dict()
        if val["id"] == amenity_id:
            if request.method == "GET":
                return jsonify(val)
        elif request.method == "DELETE":
            temp = {}
            dict_amenity[element].delete()
            storage.save()
            return jsonify(temp)
    abort(404)


@app_views.route("/amenities",
                 methods=["POST"],
                 strict_slashes=False)
def post_amenitie():
    """ Create a new item """
    data = request.get_json()
    if type(data) is not dict:
        return "Not a JSON", 400
    if "name" not in data:
        return"Missing name", 400

    new_amenity = Amenity(**data)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>",
                 methods=["PUT"],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """ Update amenity item """
    up_date = storage.get(Amenity)
    if up_date:
        data = request.get_json()
        if type(data) is dict:
            ignore = ["id", "created_at", "updated_at"]
            for k, v in data.items():
                if k not in ignore:
                    setattr(up_date, k, v)
            storage.save()
            return jsonify(up_date.to_dict()), 200
        else:
            return"Not a JSON", 400
    else:
        abort(404)