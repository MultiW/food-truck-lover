from flask import Blueprint, jsonify, request
from api.models.data import Pagination, Vendor, VendorFilter
from pydantic import ValidationError
import api.service.service as vendor_service

vendors_bp = Blueprint('vendors', __name__, url_prefix='/vendors')

@vendors_bp.route('/', methods=['POST'])
def search_vendors():
    """
    Load vendors from the external data source. Allows filtering and pagination.
    """
    try:
        # Extract pagination parameters from query string
        page = request.args.get('page', type=int)
        page_size = request.args.get('page_size', type=int)
        pagination = Pagination(page=page, page_size=page_size)

        # Get optional filters from request body
        requestBody = request.get_json(silent=True) or {}
        vendorFilter = VendorFilter(**requestBody)

    except ValidationError as e:
        raise e

    vendors: list[Vendor] = vendor_service.search_vendors(vendorFilter, pagination)
    return jsonify({"data": [v.model_dump() for v in vendors]})
