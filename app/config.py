import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "secret_key")
    SQLALCHEMY_DATABASE_URI = "sqlite:///C:/Users/DELL/Documents/3d_surface_api/instance/database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True