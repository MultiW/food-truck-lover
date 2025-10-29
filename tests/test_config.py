class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:password@db:5432/test_food_truck_lover"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
