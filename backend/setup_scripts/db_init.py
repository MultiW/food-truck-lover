import os
from sqlalchemy import create_engine
import pandas as pd
from sqlalchemy.orm import Session
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

from api.database import *  # load all DB model definitions
from api.database.base import Base
from api.database.vendor_model import VendorModel

sqlalchemy_database_uri = os.environ.get('SQLALCHEMY_DATABASE_URI')
if not sqlalchemy_database_uri:
    raise ValueError("SQLALCHEMY_DATABASE_URI environment variable not set")
engine = create_engine(sqlalchemy_database_uri)

# Create schema
metadata = Base.metadata
metadata.create_all(engine)

# Populate with data
csv_path = os.path.join(os.path.dirname(__file__), "Mobile_Food_Facility_Permit.csv")
df = pd.read_csv(csv_path)

with Session(engine) as session:
    for _, row in df.iterrows():
        lat = row['Latitude']
        lon = row['Longitude']
        if pd.notnull(lat) and pd.notnull(lon):
            point = from_shape(Point(lon, lat), srid=4326)
        else:
            point = None
        vendor = VendorModel(
            name=row['Applicant'],
            address=row['Address'],
            status=row['Status'],
            location=point
        )
        session.add(vendor)
    session.commit()
