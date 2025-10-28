import pytest
from api import create_app, db
from tests.seed_db import seed_vendors

@pytest.fixture(scope="session")
def app():
    """Create a test Flask app instance."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:password@db:5432/food_truck_lover_test"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        yield app

@pytest.fixture(scope="session")
def _db(app):
    """
    Establish a connection to the test database, create all tables, and seed test DB.
    The database is torn down at the end of the test session.
    """
    db.create_all()
    session = db.session
    seed_vendors(session)
    session.remove()
    yield db
    db.session.remove()
    db.drop_all()

@pytest.fixture(scope="function")
def db_session(_db):
    """
    Provide a transactional session for each test function that will
    automatically be rolled back. This ensures a clean database slate
    for every test.
    """
    _db.session.begin_nested()
    yield _db.session
    _db.session.rollback()

@pytest.fixture(scope="function")
def client(app, _db):
    """
    Create a test client that can be used to make requests.
    """
    return app.test_client()
