from flask import Blueprint, jsonify, request, render_template
from app.services.elevation_service import get_elevation

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

    # Generate basic 3D model data
    model_data = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [lon, lat, elevation]
        },
        "properties": {
            "elevation": elevation
        }
    }
    
    return jsonify(model_data)

@api_routes.route('/')
def home():
    return render_template('index.html')