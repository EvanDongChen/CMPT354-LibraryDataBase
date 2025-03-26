# app/__init__.py
from flask import Flask
from flask_cors import CORS
from app.extensions import db
from app.routes import api_bp
from app.models import *  # if needed
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS
    CORS(app)

    db.init_app(app)
    app.register_blueprint(api_bp)

    return app
