from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class Vendor(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)
