from api.vendors.models.data import Pagination, Vendor, VendorFilter
from api.vendors.service.sfgov_service import query_sfgov

def search_vendors(filter: VendorFilter, pagination: Pagination) -> list[Vendor]:
    data = query_sfgov({
        "query": build_query(filter),
        "page": {
            "pageNumber": pagination.page,
            "pageSize": pagination.page_size
        }
    })
    vendors = [Vendor(id=item.get('objectid'), name=item.get('applicant'), address=item.get('address')).model_dump_json() for item in data]
    return vendors

def build_query(filter: VendorFilter) -> str:
    query = "SELECT objectid, applicant, address"
    conditions = []

    if filter.vendor_name:
        conditions.append(f"UPPER(applicant) LIKE '%{filter.vendor_name.strip().upper()}%'")
    if filter.address:
        conditions.append(f"UPPER(address) LIKE '%{filter.address.strip().upper()}%'")
    #if filter.locationFilter:
    #    coord = filter.locationFilter.coordinates
    #    result_size = filter.locationFilter.result_size
    #    conditions.append(f"ST_DWithin(coordinate, ST_MakePoint({coord.longitude}, {coord.latitude})::geography, {result_size})")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    print(query)

    return query
