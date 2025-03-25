# app/__init__.py
from flask import Flask
from app.extensions import db
from app.routes import api_bp
from app.models import *  # if needed

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdb.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    app.register_blueprint(api_bp)

    return app
