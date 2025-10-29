from typing import Optional
from pydantic import BaseModel, Field
from .coordinate import Coordinate
from .enums import ApplicationStatus

class Vendor(BaseModel):
    model_config = {
        "from_attributes": True,
        "use_enum_values": True
    }
    id: int = Field(...)
    name: str = Field(...)
    address: str = Field(...)
    location: Optional[Coordinate] = Field(None)
    status: Optional[ApplicationStatus] = Field(None)

class VendorListResponse(BaseModel):
    data: list[Vendor] = Field(...)
