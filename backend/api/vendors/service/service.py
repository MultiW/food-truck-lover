from api.vendors.models.data import Pagination, Vendor, VendorFilter
from api.vendors.service.sfgov_service import query_sfgov

def search_vendors(filter: VendorFilter, pagination: Pagination) -> list[Vendor]:
    data = query_sfgov(
        query="SELECT *",
        page={
            "pageNumber": pagination.page,
            "pageSize": pagination.page_size
        }
    )
    print(data)
    vendors = [Vendor(id=item.get('objectid'), name=item.get('applicant'), address=item.get('address')).model_dump_json() for item in data]
    return vendors
