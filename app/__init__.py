from flask import Flask
from flask_sqlalchemy import SQLAlchemy 

# Initialisation de l'instance de base de données
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuration de la base de données SQLite (pour la simplicité)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialisation de la base de données
    db.init_app(app)

    return app
