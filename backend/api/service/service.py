from api.models.data import Pagination, Vendor, VendorFilter, Coordinate
from sqlalchemy import func
from api.database.vendor_model import VendorModel
from api import db
from sqlalchemy.orm import Query

SRID=4326

def search_vendors(filter: VendorFilter, pagination: Pagination) -> list[Vendor]:
    """
    Search for vendors based on the provided filter and pagination.

    Args:
        filter: VendorFilter instance containing filtering criteria
        pagination: Pagination instance containing pagination details

    Returns:
        List of Vendor instances matching the filter and pagination criteria
    """
    results: list[VendorModel] = _execute_database_query(filter, pagination)
    return _map_results_to_vendors(results)

def _execute_database_query(filter: VendorFilter, pagination: Pagination) -> list[VendorModel]:
    """
    Query to retrieve VendorModel instances based on the provided filter and pagination.
    """
    query: Query[VendorModel] = db.session.query(VendorModel)

    limit = pagination.page_size
    offset = (pagination.page - 1) * pagination.page_size

    # Apply filters
    if filter.vendor_name:
        query = query.filter(VendorModel.name.ilike(f"%{filter.vendor_name}%"))

    if filter.address:
        query = query.filter(VendorModel.address.ilike(f"%{filter.address}%"))

    # TODO apply "approved" filter

    if filter.locationFilter:
        query = _filterLocation(filter)
        # Override pagination for location-based search
        limit = filter.locationFilter.result_size
        offset = 0

    # Apply pagination
    query = query.limit(limit).offset(offset)

    return query.all()

def _filterLocation(filter: VendorFilter) -> Query[VendorModel]:
    lat = filter.locationFilter.location.latitude
    lon = filter.locationFilter.location.longitude
    target_point = func.ST_SetSRID(func.ST_MakePoint(lon, lat), SRID)
    query = db.session.query(VendorModel).order_by(VendorModel.location.op('<->')(target_point))
        
    return query

def _map_results_to_vendors(results: list[VendorModel]) -> list[Vendor]:
    """
    Map a list of VendorModel instances to a list of Vendor instances.
    """
    vendors: list[Vendor] = []
    for vendorModel in results:
        # Convert geometry to Coordinate if location is present
        location: Coordinate = None
        print("HIHI", flush=True)
        print(vendorModel, flush=True)
        if vendorModel.location:
            try:
                location = Coordinate.model_validate({
                    "latitude": vendorModel.location.y,
                    "longitude": vendorModel.location.x,
                })
            except AttributeError:
                location = None
        vendor_dict = {
            "id": vendorModel.id,
            "name": vendorModel.name,
            "address": vendorModel.address,
        }
        if location is not None:
            vendor_dict["location"] = location
        vendors.append(Vendor.model_validate(vendor_dict))
    return vendors
