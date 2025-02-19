from flask import Blueprint, jsonify, request, current_app
from app import db
from app.models import Terrain

api_routes = Blueprint('api_routes', __name__)

# Route pour obtenir tous les terrains
@api_routes.route('/terrains', methods=['GET'])
def get_terrains():
    with current_app.app_context():  # Assure l'accès à l'instance Flask
        terrains = Terrain.query.all()
        return jsonify([{
            'id': terrain.id,
            'latitude': terrain.latitude,
            'longitude': terrain.longitude,
            'altitude': terrain.altitude
        } for terrain in terrains]), 200

# Route pour ajouter un terrain
@api_routes.route('/terrain', methods=['POST'])
def add_terrain():
    data = request.get_json()
    
    # Vérification que les clés existent
    required_keys = ['latitude', 'longitude', 'altitude']
    if not all(key in data for key in required_keys):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        new_terrain = Terrain(
            latitude=float(data['latitude']),
            longitude=float(data['longitude']),
            altitude=float(data['altitude'])
        )
        db.session.add(new_terrain)
        db.session.commit()
        
        return jsonify({
            'id': new_terrain.id,
            'latitude': new_terrain.latitude,
            'longitude': new_terrain.longitude,
            'altitude': new_terrain.altitude
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
