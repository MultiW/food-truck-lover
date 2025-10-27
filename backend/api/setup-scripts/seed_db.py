from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

from api.database import * # load all DB model definitions
from api.database.base import Base

load_dotenv(override=True)

sqlalchemy_database_uri = os.environ.get('SQLALCHEMY_DATABASE_URI')
if not sqlalchemy_database_uri:
    raise ValueError("SQLALCHEMY_DATABASE_URI environment variable not set")
engine = create_engine(sqlalchemy_database_uri)

# Create schema
metadata = Base.metadata
metadata.create_all(engine)

# Populate with data
# TODO