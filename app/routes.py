import plotly.graph_objs as go
from flask import Blueprint, jsonify, request, render_template
from app import db
from app.models import Terrain
import numpy as np

api_routes = Blueprint('api_routes', __name__)

@api_routes.route('/api/terrains', methods=['GET'])
def get_terrains():
    terrains = Terrain.query.all()
    return jsonify([{
        'id': terrain.id,
        'latitude': terrain.latitude,
        'longitude': terrain.longitude,
        'altitude': terrain.altitude
    } for terrain in terrains])

@api_routes.route('/api/terrain', methods=['POST'])
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

@api_routes.route('/api/visualiser_3d', methods=['GET'])
def visualiser_3d():
    # Fetch all terrain data
    terrains = Terrain.query.all()
    
    # Extract data into lists
    latitudes = [t.latitude for t in terrains]
    longitudes = [t.longitude for t in terrains]
    altitudes = [t.altitude for t in terrains]
    
    # Check if data is sufficient
    if len(altitudes) == 0:
        return jsonify({"error": "No terrain data found"}), 404
    
    # Create a grid for the surface plot (simplified example)
    # Note: For real use, you need structured grid data (e.g., from a CSV or grid points)
    x = np.array(latitudes)
    y = np.array(longitudes)
    z = np.array(altitudes)
    
    # Reshape data into a grid (assuming data is ordered)
    # This is a simplified example; adjust based on your data structure
    grid_size = int(np.sqrt(len(z)))
    if grid_size * grid_size != len(z):
        return jsonify({"error": "Data does not form a perfect grid"}), 400
    
    z_grid = z.reshape((grid_size, grid_size))
    
    # Create 3D surface plot
    fig = go.Figure(data=[go.Surface(z=z_grid)])
    fig.update_layout(title='3D Surface Visualization', autosize=True)
    
    return render_template('visualiser_3d.html', plot=fig.to_html())