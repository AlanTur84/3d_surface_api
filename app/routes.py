from flask import Blueprint, jsonify, request, render_template
from app.services.elevation_service import get_elevations
from flask import Blueprint, jsonify, request, render_template
from app.services.elevation_service import get_elevation, get_elevations
import pandas as pd

api_routes = Blueprint('api', __name__, url_prefix='/api')

@api_routes.route('/generate_model', methods=['GET'])
def generate_3d_model():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    
    if not lat or not lon:
        return jsonify({"error": "Missing lat/lon parameters"}), 400
    
    elevation = get_elevation(lat, lon)
    if elevation is None:
        return jsonify({"error": "Failed to fetch elevation"}), 500

    return jsonify({
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [lon, lat, elevation]
        },
        "properties": {
            "elevation": elevation
        }
    })

@api_routes.route('/dataset', methods=['POST'])
def process_dataset():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
        
    try:
        file = request.files['file']
        df = pd.read_csv(file)
        
        if 'lat' not in df.columns or 'lon' not in df.columns:
            return jsonify({"error": "CSV must contain 'lat' and 'lon' columns"}), 400

        coordinates = list(zip(df['lat'], df['lon']))
        elevations = get_elevations(coordinates)
        
        if None in elevations:
            return jsonify({"error": "Failed to fetch some elevation data"}), 500

        return jsonify({
            "type": "FeatureCollection",
            "features": [
                {
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lon, lat, elev]
                    },
                    "properties": {
                        "elevation": elev
                    }
                }
                for (lat, lon), elev in zip(coordinates, elevations)
            ]
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_routes.route('/')
def home():
    return render_template('index.html')