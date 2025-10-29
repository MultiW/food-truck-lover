import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database

from tests.test_config import TestConfig
from tests.seed_db import seed_database
from api import create_app, db

from api.database import *  # load all DB model definitions
from api.database.base import Base

@pytest.fixture(scope="session")
def app():
    """
    Create a test Flask app instance.
    Set up and tear down the test database.
    """
    if database_exists(TestConfig.SQLALCHEMY_DATABASE_URI):
        drop_database(TestConfig.SQLALCHEMY_DATABASE_URI)
    create_database(TestConfig.SQLALCHEMY_DATABASE_URI)

    app = create_app(TestConfig)

    # Create schema and seed data
    with app.app_context():
        with db.engine.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis;"))
            conn.commit()

        db.create_all()  # create schema
        seed_database()

    yield app

    with app.app_context():
        db.engine.dispose()  # close connections
    drop_database(TestConfig.SQLALCHEMY_DATABASE_URI)

@pytest.fixture(scope="function")
def client(app):
    """
    Create a test client that can be used to make requests.
    """
    return app.test_client()
