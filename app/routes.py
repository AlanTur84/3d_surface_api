import csv
import numpy as np
from io import TextIOWrapper
from flask import Blueprint, jsonify, request, render_template
from app import db
from app.models import Terrain
import plotly.graph_objs as go

api_routes = Blueprint('api_routes', __name__)

@api_routes.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@api_routes.route('/api/upload_csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    csv_file = request.files['file']
    if csv_file.filename == '':
        return jsonify({"error": "Empty filename"}), 400
    
    try:
        csv_data = TextIOWrapper(csv_file, encoding='utf-8')
        reader = csv.DictReader(csv_data)
        
        # Validate CSV columns
        required_columns = ['latitude', 'longitude', 'altitude']
        if not all(col in reader.fieldnames for col in required_columns):
            return jsonify({"error": "CSV must contain 'latitude', 'longitude', and 'altitude' columns"}), 400
        
        # Clear existing data (optional)
        Terrain.query.delete()
        
        # Insert new data
        for row in reader:
            terrain = Terrain(
                latitude=float(row['latitude']),
                longitude=float(row['longitude']),
                altitude=float(row['altitude'])
            )
            db.session.add(terrain)
        
        db.session.commit()
        return jsonify({"message": f"CSV uploaded successfully ({reader.line_num - 1} rows)"}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@api_routes.route('/api/visualiser_3d', methods=['GET'])
def visualiser_3d():
    terrains = Terrain.query.all()
    
    # Extract data
    latitudes = [t.latitude for t in terrains]
    longitudes = [t.longitude for t in terrains]
    altitudes = [t.altitude for t in terrains]
    
    # Validate grid structure
    grid_size = int(np.sqrt(len(altitudes)))
    if grid_size ** 2 != len(altitudes):
        return render_template('error.html', error="Data does not form a perfect grid (e.g., 10x10 points)")
    
    # Reshape into grid
    x = np.array(latitudes).reshape((grid_size, grid_size))
    y = np.array(longitudes).reshape((grid_size, grid_size))
    z = np.array(altitudes).reshape((grid_size, grid_size))
    
    # Generate plot
    fig = go.Figure(data=[go.Surface(x=x, y=y, z=z)])
    fig.update_layout(
        title='3D Terrain Surface',
        scene=dict(
            xaxis_title='Latitude',
            yaxis_title='Longitude',
            zaxis_title='Altitude'
        )
    )
    
    return render_template('visualiser_3d.html', plot=fig.to_html())