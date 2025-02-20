# app/routes.py
from flask import Blueprint, jsonify, request, render_template
from app.services.elevation_service import get_elevations
import pandas as pd
import io
import logging
import traceback
import chardet  # Add this new import

api_routes = Blueprint('api', __name__, url_prefix='/api')

@api_routes.route('/dataset', methods=['POST'])
def handle_dataset():
    try:
        if 'dataset' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
            
        file = request.files['dataset']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
            
        if not file.filename.endswith('.csv'):
            return jsonify({"error": "Only CSV files allowed"}), 400

        try:
            # Detect file encoding
            raw_data = file.stream.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding'] or 'utf-8'
            
            # Reset stream and read with detected encoding
            file.stream.seek(0)
            content = raw_data.decode(encoding, errors='replace')
            
            df = pd.read_csv(io.StringIO(content))
            
            if not {'lat', 'lon'}.issubset(df.columns):
                return jsonify({"error": "CSV must contain 'lat' and 'lon' columns"}), 400
                
            coordinates = list(zip(df['lat'], df['lon']))
            elevations = get_elevations(coordinates)
            
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
                    "encoding_used": encoding  # Return detected encoding
                },
                "features": features
            })
            
        except pd.errors.ParserError:
            return jsonify({"error": "Invalid CSV format"}), 400
        except UnicodeDecodeError as ude:
            logging.error(f"Encoding error: {str(ude)}")
            return jsonify({"error": "Invalid file encoding. Try saving as UTF-8"}), 400
            
    except Exception as e:
        logging.error(f"Error: {traceback.format_exc()}")
        return jsonify({"error": "Internal server error"}), 500

@api_routes.route('/')
def home():
    return render_template('index.html')