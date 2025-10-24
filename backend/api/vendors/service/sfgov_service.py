import requests
from flask import current_app

def query_sfgov(query: str, page: dict) -> dict:
    """
    Utility to make a POST request to the SFGov API.
    Handles URL construction and token fetching.
    Args:
        query (str): SQL query string.
        page (dict): Dict with 'pageNumber' and 'pageSize'.
    Returns:
        dict: JSON response from SFGov API.
    """
    app_token = current_app.config['DATASF_APP_TOKEN']
    url = f'https://data.sfgov.org/api/v3/views/rqzj-sfat/query.json?app_token={app_token}'
    body = {
        "query": query,
        "page": page
    }
    response = requests.post(url, json=body)
    response.raise_for_status()
    return response.json()
