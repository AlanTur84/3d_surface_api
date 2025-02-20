from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configure upload settings
    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB limit
    app.config['ALLOWED_EXTENSIONS'] = {'csv'}
    
    db.init_app(app)

    with app.app_context():
        from . import routes
        db.create_all()
        app.register_blueprint(routes.api_routes)

    return app