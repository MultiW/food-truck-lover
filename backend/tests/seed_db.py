from api.database.vendor_model import VendorModel
from api.models.data import ApplicationStatus
import json

def seed_vendors(db_session):
    """
    Adds a set of predefined vendors to the database.
    """
    vendors: list[VendorModel] = load_vendors_from_json("tests/test_data.json")
    db_session.add_all(vendors)
    db_session.commit()

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
        vendor = VendorModel(
            name=v["name"],
            address=v["address"],
            status=ApplicationStatus[v["status"]],
            location=v["location"]
        )
        vendors.append(vendor)
    return vendors