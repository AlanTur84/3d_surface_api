import plotly.graph_objs as go
from flask import Blueprint, jsonify, request, render_template
from app import db
from app.models import Terrain

api_routes = Blueprint('api_routes', __name__)

# Route pour obtenir tous les terrains (reste inchangée)
@api_routes.route('/terrains', methods=['GET'])
def get_terrains():
    terrains = Terrain.query.all()
    return jsonify([{
        'id': terrain.id,
        'latitude': terrain.latitude,
        'longitude': terrain.longitude,
        'altitude': terrain.altitude
    } for terrain in terrains])

# Route pour ajouter un terrain (reste inchangée)
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

# Nouvelle route pour visualiser les terrains en 3D
@api_routes.route('/visualiser_3d/<int:id>', methods=['GET'])
def visualiser_3d(id):
    terrain = Terrain.query.get(id)
    if terrain:
        # Passer les données du terrain à la template pour affichage
        return render_template('visualiser_3d.html', terrain=terrain)
    else:
        return jsonify({"error": "Terrain not found"}), 404