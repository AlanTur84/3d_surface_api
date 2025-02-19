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
@api_routes.route('/visualiser_3d', methods=['GET'])
def visualiser_3d():
    # Récupérer tous les terrains depuis la base de données
    terrains = Terrain.query.all()

    # Extraire les coordonnées et altitudes
    latitudes = [terrain.latitude for terrain in terrains]
    longitudes = [terrain.longitude for terrain in terrains]
    altitudes = [terrain.altitude for terrain in terrains]

    # Créer une trace 3D pour afficher les terrains
    trace = go.Scatter3d(
        x=longitudes,
        y=latitudes,
        z=altitudes,
        mode='markers',
        marker=dict(size=5, color=altitudes, colorscale='Viridis', opacity=0.8)
    )

    # Définir la mise en page de la visualisation 3D
    layout = go.Layout(
        title='3D Terrain Visualization',
        scene=dict(
            xaxis_title='Longitude',
            yaxis_title='Latitude',
            zaxis_title='Altitude'
        )
    )

    # Créer la figure Plotly avec la trace et la mise en page
    fig = go.Figure(data=[trace], layout=layout)

    # Convertir la figure en HTML pour l'affichage dans le template
    graph_html = fig.to_html(full_html=False)

    # Retourner le template avec le graphique intégré
    return render_template('visualiser_3d.html', graph_html=graph_html)
