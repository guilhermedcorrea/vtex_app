from flask import Flask
from ..config import SQLALCHEMY_DATABASE_URI
import secrets
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .extensions import db



migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SECRET_KEY'] = secrets.token_hex()
    app.config['SQLALCHEMY_POOL_SIZE'] = 370
    app.config['SQLALCHEMY_MAX_OVERFLOW'] = 0
    app.config['DEBUG'] = True
    
   
    with app.app_context():
        db.init_app(app)
        from .admin.admin import vtex
        migrate.init_app(app, db)
        app.register_blueprint(vtex)
        
    return app