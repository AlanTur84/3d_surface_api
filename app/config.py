import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "secret_key")
    SQLALCHEMY_DATABASE_URI = "sqlite:///instance/database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True