from flask import Blueprint, jsonify, request, render_template
from app.services.elevation_service import get_elevations
import pandas as pd
import io

api_routes = Blueprint('api', __name__, url_prefix='/api')

@api_routes.route('/dataset', methods=['POST'])
def handle_dataset():
    # Check if file was uploaded
    if 'dataset' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
        
    file = request.files['dataset']
    
    # Check if file is selected
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Validate file type
    if not file.filename.endswith('.csv'):
        return jsonify({"error": "Only CSV files are allowed"}), 400
    
    try:
        # Read CSV directly from file stream
        df = pd.read_csv(io.StringIO(file.stream.read().decode('UTF-8')))
        
        # Validate required columns
        if not {'lat', 'lon'}.issubset(df.columns):
            return jsonify({"error": "CSV must contain 'lat' and 'lon' columns"}), 400
            
        # Convert to coordinate pairs
        coordinates = list(zip(df['lat'], df['lon']))
        
        # Batch elevation lookup
        elevations = get_elevations(coordinates)
        
        # Check for failed elevations
        if None in elevations:
            failed = sum(1 for e in elevations if e is None)
            return jsonify({
                "error": f"Failed to get elevation for {failed} points",
                "successful": len(elevations) - failed
            }), 207  # Multi-status code
            
        # Create GeoJSON response
        features = [
            {
                "type": "Feature",
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
        
        return jsonify({
            "type": "FeatureCollection",
            "metadata": {
                "point_count": len(features),
                "min_elevation": min(elevations),
                "max_elevation": max(elevations)
            },
            "features": features
        })
        
    except pd.errors.ParserError:
        return jsonify({"error": "Invalid CSV format"}), 400
    except Exception as e:
        return jsonify({"error": f"Processing error: {str(e)}"}), 500

@api_routes.route('/generate_model', methods=['GET'])
def generate_3d_model():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    
    if not lat or not lon:
        return jsonify({"error": "Missing lat/lon parameters"}), 400
    
    elevation = get_elevations([(lat, lon)])[0]
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

@api_routes.route('/')
def home():
    return render_template('index.html')