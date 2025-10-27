from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base
from geoalchemy2 import Geometry

class VendorModel(Base):
    __tablename__ = 'vendor'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
    location: Mapped[Geometry] = mapped_column(Geometry(geometry_type='POINT', srid=4326, spatial_index=True))
