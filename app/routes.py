from flask import Blueprint, jsonify, request, render_template
from app.services.elevation_service import get_elevations
import pandas as pd
import io
import logging
import traceback

api_routes = Blueprint('api', __name__, url_prefix='/api')

@api_routes.route('/dataset', methods=['POST'])
def handle_dataset():
    try:
        # Validate file existence
        if 'dataset' not in request.files:
            logging.error("No file part in request")
            return jsonify({"error": "No file uploaded"}), 400
            
        file = request.files['dataset']
        
        # Validate file selection
        if file.filename == '':
            logging.error("Empty filename submitted")
            return jsonify({"error": "Please select a file"}), 400
            
        # Validate file type
        if not file.filename.lower().endswith('.csv'):
            logging.error(f"Invalid file type: {file.filename}")
            return jsonify({"error": "Only CSV files allowed"}), 400

        # Read and validate CSV
        try:
            content = file.stream.read().decode('utf-8')
            df = pd.read_csv(io.StringIO(content))
            
            # Check for required columns
            if not {'lat', 'lon'}.issubset(df.columns):
                missing = [c for c in ['lat', 'lon'] if c not in df.columns]
                logging.error(f"Missing columns: {missing}")
                return jsonify({
                    "error": f"Missing required columns: {', '.join(missing)}"
                }), 400
                
            # Validate coordinate ranges
            if (df['lat'].abs() > 90).any() or (df['lon'].abs() > 180).any():
                logging.error("Invalid coordinate values")
                return jsonify({
                    "error": "Invalid coordinates (lat: -90 to 90, lon: -180 to 180)"
                }), 400

        except pd.errors.ParserError as e:
            logging.error(f"CSV parsing error: {str(e)}")
            return jsonify({"error": "Invalid CSV format"}), 400
        except UnicodeDecodeError:
            logging.error("Invalid file encoding")
            return jsonify({"error": "Invalid file encoding (use UTF-8)"}), 400

        # Process coordinates
        coordinates = list(zip(df['lat'], df['lon']))
        logging.info(f"Processing {len(coordinates)} coordinates")
        
        # Get elevations with error handling
        elevations = get_elevations(coordinates)
        success_rate = sum(e is not None for e in elevations) / len(elevations)
        
        if success_rate < 0.5:
            logging.warning(f"Low elevation success rate: {success_rate*100}%")

        # Build response
        features = []
        for (lat, lon), elev in zip(coordinates, elevations):
            if elev is not None:
                features.append({
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
                "successful_points": len(features),
                "min_elevation": min(e['properties']['elevation'] for e in features),
                "max_elevation": max(e['properties']['elevation'] for e in features)
            },
            "features": features
        })

    except Exception as e:
        logging.error(f"Unexpected error: {traceback.format_exc()}")
        return jsonify({"error": "Internal server error"}), 500

# Keep other routes unchanged from previous version