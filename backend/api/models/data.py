from pydantic import BaseModel, Field

class Coordinate(BaseModel):
    latitude: float = Field(..., ge=-90, le=90, description="Latitude must be between -90 and 90")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude must be between -180 and 180")

class LocationFilter(BaseModel):
    location: Coordinate = Field(..., description="Coordinates are required for location filter")
    result_size: int = Field(..., gt=0, le=10000, description="Result size must be between 1 and 10,000")

class Pagination(BaseModel):
    page: int = Field(..., gt=0, description="Page number must be positive")
    page_size: int = Field(..., gt=0, description="Page size must be positive")

class VendorFilter(BaseModel):
    vendor_name: str = Field(None, description="Vendor name filter")
    address: str = Field(None, description="Address filter")
    locationFilter: LocationFilter = Field(None, description="Location-based filter")

class Vendor(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    address: str = Field(...)
    location: Coordinate = Field(None)