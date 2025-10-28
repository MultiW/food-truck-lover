from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import Config

from api.database.base import Base
db = SQLAlchemy(model_class=Base)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from api.routes import vendors_bp
    app.register_blueprint(vendors_bp)

    from api.errors import errors_bp
    app.register_blueprint(errors_bp)

    db.init_app(app)

    return app