from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app.models import db
from app.routes import init_app as init_routes
def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    CORS(app)
    
    
    db.init_app(app)
    
    
    init_routes(app)

    with app.app_context():
        db.create_all()

    return app