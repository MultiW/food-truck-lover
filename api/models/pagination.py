from pydantic import BaseModel, Field

class Pagination(BaseModel):
    page: int = Field(..., gt=0, description="Page number to retrieve using 1-based indexing")
    page_size: int = Field(..., gt=0, description="Size of each page")
