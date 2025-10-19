from dotenv import load_dotenv
load_dotenv(override=True)
# TODO: set PYTHON_DOTENV_DISABLED=1 to disable in production

from flask import Flask
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from api.vendors.routes import vendors_bp
    app.register_blueprint(vendors_bp)

    return app
