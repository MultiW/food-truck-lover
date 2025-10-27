import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATASF_APP_TOKEN = os.environ.get('DATASF_APP_TOKEN')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')