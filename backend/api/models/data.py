import enum
from typing import Optional
from pydantic import BaseModel, Field

class ApplicationStatus(enum.Enum):
    APPROVED = "APPROVED"
    REQUESTED = "REQUESTED"
    ISSUED = "ISSUED"
    EXPIRED = "EXPIRED"
    SUSPEND = "SUSPEND"

class Coordinate(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

class LocationFilter(BaseModel):
    location: Coordinate = Field(...)
    result_size: int = Field(..., gt=0, le=10000, description="Number of nearest vendors to return. Overrides the main filter pagination.")

class Pagination(BaseModel):
    page: int = Field(..., gt=0, description="Page number to retrieve using 1-based indexing")
    page_size: int = Field(..., gt=0, description="Size of each page")

class VendorFilter(BaseModel):
    vendor_name: Optional[str] = Field(None, description="Vendor name case insensitive partial match")
    address: Optional[str] = Field(None, description="Address case insensitive partial match")
    locationFilter: Optional[LocationFilter] = Field(None)
    status: Optional[ApplicationStatus] = Field(None)

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