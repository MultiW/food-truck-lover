from flask import Blueprint, jsonify, current_app
import requests

vendors_bp = Blueprint('vendors', __name__, url_prefix='/vendors')

@vendors_bp.route('/', methods=['GET'])
def vendors():
    """
    Load vendors from the external data source. Allows filtering and pagination.
    """
    # TODO
    response = requests.get(
        'https://data.sfgov.org/api/v3/views/rqzj-sfat/query.json?app_token=' + current_app.config['DATASF_APP_TOKEN']
    )
    response.raise_for_status()
    return response.json()

@vendors_bp.route('/nearby', methods=['POST'])
def vendors_nearby():
    """
    Load nearby vendors based on provided coordinates.
    """
    # TODO
    return jsonify({})
