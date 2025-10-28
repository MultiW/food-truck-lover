from flask import Blueprint, jsonify
from pydantic_core import ValidationError

errors_bp = Blueprint('errors_bp', __name__)

@errors_bp.app_errorhandler(Exception)
def handle_any_exception(error):
    """Handler for all other global exceptions."""
    response = {
        'status': 'error',
        'message': 'An internal server error occurred. Please try again later.',
        'details': str(error)
    }
    return jsonify(response), 500

@errors_bp.app_errorhandler(ValidationError)
def handle_pydantic_validation_error(error):
    """Global handler for Pydantic validation errors."""
    response = {
        'code': '400',
        'message': 'Request body validation failed',
        'details': str(error)
    }
    return jsonify(response), 400
