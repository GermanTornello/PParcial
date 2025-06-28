from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    from config.config import Config
    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)

    from models.cancion import Cancion
    from routes.cancion import bp as canciones_bp

    with app.app_context():
        db.create_all()

    app.register_blueprint(canciones_bp)

    @app.route('/')
    def home():
        return "¡Bienvenido a la API de Spotify!"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
