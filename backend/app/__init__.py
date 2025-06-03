from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from app.routes import api_bp
from app.models import *  # if needed
from config import Config
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder=None)  # Disable Flask's default static handler
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    # Configure CORS
    CORS(app, 
         resources={
             r"/*": {
                 "origins": [
                     "http://localhost:3000",
                     "http://localhost:5000",
                     "http://127.0.0.1:3000",
                     "http://127.0.0.1:5000"
                 ],
                 "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                 "allow_headers": ["Content-Type", "Authorization"],
                 "supports_credentials": True,
                 "expose_headers": ["Content-Type", "Authorization"],
                 "max_age": 600
             }
         })

    # Register blueprints
    app.register_blueprint(api_bp)

    # Serve static files from React build
    @app.route('/static/<path:filename>')
    def serve_static(filename):
        build_dir = os.path.join(app.root_path, '..', 'build', 'static')
        file_path = os.path.join(build_dir, filename)
        print(f"Serving static file: {file_path}")  # Debug print
        return send_from_directory(build_dir, filename)

    # Serve React build files (catch-all)
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_react(path):
        build_dir = os.path.join(app.root_path, '..', 'build')
        file_path = os.path.join(build_dir, path)
        print(f"Serving from React build: {file_path}")  # Debug print
        if path != "" and os.path.exists(file_path):
            return send_from_directory(build_dir, path)
        else:
            return send_from_directory(build_dir, 'index.html')

    return app