from flask_sqlalchemy import SQLAlchemy
from api.database.base import Base

from flask import Flask
from config import Config

db = SQLAlchemy(model_class=Base)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from api.routes import vendors_bp
    app.register_blueprint(vendors_bp)

    db.init_app(app)

    return app