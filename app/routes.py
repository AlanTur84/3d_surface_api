from flask import Blueprint, jsonify, request, render_template
from app.services.elevation_service import get_elevations
import pandas as pd
import io
import logging

api_routes = Blueprint('api', __name__, url_prefix='/api')

@api_routes.route('/generate_model', methods=['GET'])
def generate_3d_model():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    
    if not lat or not lon:
        return jsonify({"error": "Missing lat/lon parameters"}), 400
    
    try:
        elevation = get_elevations([(lat, lon)])[0]
        if elevation is None:
            raise ValueError("Elevation service failed")
            
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
        
    except Exception as e:
        logging.error(f"Single point error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@api_routes.route('/dataset', methods=['POST'])
def handle_dataset():
    if 'dataset' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
        
    file = request.files['dataset']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if not file.filename.endswith('.csv'):
        return jsonify({"error": "Only CSV files allowed"}), 400

    try:
        # Read and validate CSV
        df = pd.read_csv(io.StringIO(file.stream.read().decode('utf-8')))
        
        if not {'lat', 'lon'}.issubset(df.columns):
            return jsonify({"error": "CSV must contain 'lat' and 'lon' columns"}), 400
            
        # Process coordinates
        coordinates = list(zip(df['lat'], df['lon']))
        elevations = get_elevations(coordinates)
        
        # Handle partial failures
        successful = []
        for (lat, lon), elev in zip(coordinates, elevations):
            if elev is not None:
                successful.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lon, lat, elev]
                    },
                    "properties": {"elevation": elev}
                })

        return jsonify({
            "type": "FeatureCollection",
            "metadata": {
                "total_points": len(coordinates),
                "successful_points": len(successful),
                "failed_points": len(coordinates) - len(successful)
            },
            "features": successful
        })
        
    except pd.errors.ParserError:
        return jsonify({"error": "Invalid CSV format"}), 400
    except Exception as e:
        logging.error(f"Dataset error: {str(e)}")
        return jsonify({"error": "Processing failed"}), 500

@api_routes.route('/')
def home():
    return render_template('index.html')