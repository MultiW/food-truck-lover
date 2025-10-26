import requests
from flask import current_app

def query_sfgov(request_body: str) -> dict:
    """
    Utility to query the SFGov API.
    Handles URL construction and token fetching.
    Args:
        request_body (str): REST API request body.
    Returns:
        dict: JSON response from SFGov API.
    """
    app_token = current_app.config['DATASF_APP_TOKEN']
    url = f'https://data.sfgov.org/api/v3/views/rqzj-sfat/query.json?app_token={app_token}'
    response = requests.post(url, json=request_body)
    response.raise_for_status()
    return response.json()
