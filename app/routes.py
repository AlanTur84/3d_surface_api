from flask import Blueprint, jsonify, request
from app import db
from app.models import Terrain

api_routes = Blueprint('api_routes', __name__)

# Route pour obtenir tous les terrains
@api_routes.route('/terrains', methods=['GET'])
def get_terrains():
    terrains = Terrain.query.all()
    return jsonify([{
        'id': terrain.id,
        'latitude': terrain.latitude,
        'longitude': terrain.longitude,
        'altitude': terrain.altitude
    } for terrain in terrains])

# Route pour ajouter un terrain
@api_routes.route('/terrain', methods=['POST'])
def add_terrain():
    data = request.get_json()
    new_terrain = Terrain(
        latitude=data['latitude'],
        longitude=data['longitude'],
        altitude=data['altitude']
    )
    db.session.add(new_terrain)
    db.session.commit()
    return jsonify({
        'id': new_terrain.id,
        'latitude': new_terrain.latitude,
        'longitude': new_terrain.longitude,
        'altitude': new_terrain.altitude
    }), 201
