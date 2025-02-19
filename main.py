from flask import Flask
from app.routes import api_routes

app = Flask(__name__)

# Enregistrement des routes de l'API
app.register_blueprint(api_routes, url_prefix='/api')

if __name__ == "__main__":
    app.run(debug=True)
