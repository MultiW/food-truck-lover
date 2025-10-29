import json
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

from api import db
from api.database.vendor_model import VendorModel
from api.models.enums import ApplicationStatus

def seed_database():
    """
    Adds a set of predefined vendors to the database.
    """
    vendors: list[VendorModel] = load_vendors_from_json("tests/test_data.json")
    db.session.add_all(vendors)
    db.session.commit()

def load_vendors_from_json(json_path: str) -> list[VendorModel]:
    """
    Load vendor data from the given JSON path.

    Args:
        json_path: Path to the JSON file containing vendor data.
    Returns:
        List of VendorModel instances.
    """
    with open(json_path) as f:
        vendor_data = json.load(f)
    vendors: list[VendorModel] = []
    for v in vendor_data:
        lat = v['location']['latitude']
        lon = v['location']['longitude']
        point = from_shape(Point(lon, lat), srid=4326)
        vendor = VendorModel(
            name=v["name"],
            address=v["address"],
            status=ApplicationStatus[v["status"]],
            location=point
        )
        vendors.append(vendor)
    return vendors