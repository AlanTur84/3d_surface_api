import os

class Config:
    """Configuration de l'application Flask"""
    
    # Clé secrète pour la sécurité
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")

    # Configuration de la base de données SQLite
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuration pour le mode de débogage
    DEBUG = os.getenv("FLASK_DEBUG", "True") == "True"
