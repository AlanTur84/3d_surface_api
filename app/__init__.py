from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config  # Importation de la config

# Initialisation de l'instance de base de données
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Charger la configuration depuis config.py
    app.config.from_object(Config)

    # Initialisation de la base de données
    db.init_app(app)

    # Enregistrer les routes
    with app.app_context():
        from . import routes  # Importation des routes
        db.create_all()  # Création automatique des tables

    return app
