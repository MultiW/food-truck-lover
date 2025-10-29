from flask import Blueprint, jsonify, request
from flask_pydantic_spec import Response, Request
from pydantic import ValidationError

from api.models.filters import VendorFilter
from api.models.pagination import Pagination
from api.models.vendor import VendorListResponse
import api.service.service as vendor_service
from api import spec

vendors_bp = Blueprint('vendors', __name__, url_prefix='/vendors')

@vendors_bp.route('/', methods=['POST'])
@spec.validate(query=Pagination, body=Request(VendorFilter), resp=Response(HTTP_200=VendorListResponse))
def search_vendors():
    try:
        pagination = request.context.query  # required pagination parameters
        vendorFilter = request.context.body or {}  # optional filter parameters
    except ValidationError as e:
        raise e

    vendors: VendorListResponse = VendorListResponse(data=vendor_service.search_vendors(vendorFilter, pagination))
    return jsonify(vendors.model_dump())
