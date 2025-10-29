from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_pydantic_spec import FlaskPydanticSpec

from config import Config
from api.database.base import Base

db = SQLAlchemy(model_class=Base)
spec = FlaskPydanticSpec('backend', title='Vendor Search API')

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # API routes registration
    from api.routes import vendors_bp
    app.register_blueprint(vendors_bp)

    from api.errors import errors_bp
    app.register_blueprint(errors_bp)

    # DB setup
    db.init_app(app)

    # API documentation setup
    spec.register(app)

    return app
