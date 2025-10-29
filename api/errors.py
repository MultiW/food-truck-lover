from flask import Blueprint, jsonify

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
