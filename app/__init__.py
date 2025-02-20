from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad request"}), 400

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Elevation service unavailable"}), 500

    with app.app_context():
        from . import routes
        db.create_all()
        app.register_blueprint(routes.api_routes)

    return app