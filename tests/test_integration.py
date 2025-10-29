# ============================
# === Test Filter Validity ===
# ============================
def test_pagination_validation(client):
    """
    Test that pagination is required and missing pagination returns a 400 error.
    """
    response = client.post('/vendors/', json={})
    assert response.status_code == 422

def test_pagination_works(client):
    """
    Test that pagination returns the correct number of results and correct page.
    """
    # Page 2, page_size 3
    response = client.post('/vendors/?page=2&page_size=3')
    assert response.status_code == 200
    ids = [v["id"] for v in response.json["data"]]
    assert ids == [4, 5, 6]

    # Page 4, page_size 3
    response = client.post('/vendors/?page=4&page_size=3')
    assert response.status_code == 200
    ids = [v["id"] for v in response.json["data"]]
    assert ids == [10]


def test_location_filter_validation(client):
    """
    Test that location filter requires latitude, longitude, and result_size fields.
    """
    # Missing latitude
    bad_location_lat = {
        "locationFilter": {
            "location": {
                "longitude": 20
            },
            "result_size": 5
        }
    }
    response = client.post('/vendors/?page=1&page_size=10', json=bad_location_lat)
    assert response.status_code == 422

    # Missing longitude
    bad_location_lon = {
        "locationFilter": {
            "location": {
                "latitude": 10
            },
            "result_size": 5
        }
    }
    response = client.post('/vendors/?page=1&page_size=10', json=bad_location_lon)
    assert response.status_code == 422

    # Missing result_size
    bad_location_rs = {
        "locationFilter": {
            "location": {
                "latitude": 10,
                "longitude": 20
            }
        }
    }
    response = client.post('/vendors/?page=1&page_size=10', json=bad_location_rs)
    assert response.status_code == 422

# ==================================
# === Test Filters Functionality ===
# ==================================
def test_vendor_name_filter(client):
    """
    Test vendor_name filter for partial and case-insensitive match
    ."""
    response = client.post('/vendors/?page=1&page_size=10', json={"vendor_name": "tasty"})
    assert response.status_code == 200
    ids = set([v["id"] for v in response.json["data"]])
    assert ids == {1}  # Tasty Truck

def test_status_filter(client):
    """
    Test status filter returns only vendors with APPROVED status.
    """
    response = client.post('/vendors/?page=1&page_size=10', json={"status": "APPROVED"})
    assert response.status_code == 200
    ids = [v["id"] for v in response.json["data"]]
    assert set(ids) == {1, 2, 3, 4, 5}

def test_address_filter(client):
    """
    Test address filter for partial and case-insensitive match.
    """
    response = client.post('/vendors/?page=1&page_size=10', json={"address": "main"})
    assert response.status_code == 200
    ids = set([v["id"] for v in response.json["data"]])
    assert ids == {1}  # 123 Main St

def test_location_filter(client):
    """
    Test location filter returns closest vendors, ignoring pagination.
    """
    location_filter = {
        "locationFilter": {
            "location": {"latitude": -40, "longitude": 40},
            "result_size": 3
        }
    }
    response = client.post('/vendors/?page=1&page_size=10', json=location_filter)
    assert response.status_code == 200
    ids = set([v["id"] for v in response.json["data"]])
    assert ids == {1, 2, 3}  # Closest to (-40, 40)

def test_location_and_status_filter(client):
    """
    Test location filter combined with status filter.
    """
    location_filter = {
        "locationFilter": {
            "location": {"latitude": -40, "longitude": 40},
            "result_size": 5
        },
        "status": "REQUESTED"
    }
    response = client.post('/vendors/?page=1&page_size=10', json=location_filter)
    assert response.status_code == 200
    ids = set([v["id"] for v in response.json["data"]])
    assert ids == {6, 10}

def test_location_and_name_filter(client):
    """
    Test location filter combined with vendor_name filter.
    """
    location_filter = {
        "locationFilter": {
            "location": {"latitude": -40, "longitude": 40},
            "result_size": 2
        },
        "vendor_name": "tasty"
    }
    response = client.post('/vendors/?page=1&page_size=10', json=location_filter)
    assert response.status_code == 200
    ids = set([v["id"] for v in response.json["data"]])
    assert ids == {1}

def test_location_and_address_filter(client):
    """
    Test location filter combined with address filter.
    """
    location_filter = {
        "locationFilter": {
            "location": {"latitude": -40, "longitude": 40},
            "result_size": 2
        },
        "address": "main"
    }
    response = client.post('/vendors/?page=1&page_size=10', json=location_filter)
    assert response.status_code == 200
    ids = set([v["id"] for v in response.json["data"]])
    assert ids == {1}
