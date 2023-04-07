Copy code
#!/usr/bin/python3
"""Module for Places amenities API"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, Place, Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_amenities_by_place(place_id):
    """Retrieve a list of amenities of a place"""
    place = storage.get('Place', place_id)
    if not place:
        abort(404, 'Not found')
    if storage.__class__.__name__ == 'DBStorage':
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [storage.get('Amenity', id).to_dict()
                     for id in place.amenity_ids]
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """Delete an amenity from a place"""
    place = storage.get('Place', place_id)
    amenity = storage.get('Amenity', amenity_id)
    if not place:
        abort(404, 'Not found')
    if not amenity:
        abort(404, 'Not found')
    if storage.__class__.__name__ == 'DBStorage':
        if amenity not in place.amenities:
            abort(404, 'Not found')
        place.amenities.remove(amenity)
        storage.save()
    else:
        if amenity_id not in place.amenity_ids:
            abort(404, 'Not found')
        place.amenity_ids.remove(amenity_id)
        place.save()
    return jsonify({})


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def link_amenity_to_place(place_id, amenity_id):
    """Link an amenity to a place"""
    place = storage.get('Place', place_id)
    amenity = storage.get('Amenity', amenity_id)
    if not place:
        abort(404, 'Not found')
    if not amenity:
        abort(404, 'Not found')
    if storage.__class__.__name__ == 'DBStorage':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
        storage.save()
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)
        place.save()
    return jsonify(amenity.to_dict()), 201