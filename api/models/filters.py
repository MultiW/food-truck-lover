from typing import Optional
from pydantic import BaseModel, Field
from .coordinate import Coordinate
from .enums import ApplicationStatus

class LocationFilter(BaseModel):
    location: Coordinate = Field(...)
    result_size: int = Field(..., gt=0, le=10000, description="Number of nearest vendors to return. Overrides the main filter pagination.")

class VendorSearchRequest(BaseModel):
    vendor_name: Optional[str] = Field(None, description="Vendor name case insensitive partial match")
    address: Optional[str] = Field(None, description="Address case insensitive partial match")
    locationFilter: Optional[LocationFilter] = Field(None)
    status: Optional[ApplicationStatus] = Field(None)
