# Food Truck Map

[_Link to project GitHub repository_](https://github.com/MultiW/food-truck-map)

This project is a backend API for searching Mobile Food Facilities in San Francisco, using the public dataset: [Mobile Food Facility Permit](https://data.sfgov.org/Economy-and-Community/Mobile-Food-Facility-Permit/rqzj-sfat/about_data).

## Problem

Food lovers often struggle to discover nearby food trucks in real time. While platforms like Google Maps or Yelp make it easy to find brick-and-mortar restaurants, they fall short when it comes to mobile vendors. As a result, hungry customers miss out on great local eats, and food truck owners lose valuable opportunities to reach potential customers.

## Solution

This project leverages San Francisco’s [Mobile Food Facility Permit](https://data.sfgov.org/Economy-and-Community/Mobile-Food-Facility-Permit/rqzj-sfat/about_data) dataset to help users discover mobile food vendors across the city. It implements the backend foundation of a broader platform designed to make food trucks more accessible and visible. The service provides search and filtering capabilities based on vendor name, street, or geographic coordinates. This lays the groundwork for an eventual web application where users can explore nearby food trucks on an interactive map.

## Technical Solution

### Tech Stack

- **Backend and REST API Framework**: Flask (Python)
- **Database**: PostgreSQL with PostGIS extension
- **Containerization**: Docker
- **Other**
  - **Backend Model Validation**: Pydantic
  - **SQL Toolkit and ORM**: Flask-SQLAlchemy

### Tech Stack Reasoning

- **Flask**: A lightweight, unopinionated framework that enables rapid prototyping while providing full control over routing and request handling. Its simplicity makes it ideal for quickly standing up a clean, testable REST API.

- **PostgreSQL and PostGIS**:
  - We chose to host our own database as opposed to querying the DataSF dataset. This allows us to scale without being bottlenecked by the DataSF servers and allows us to implement our own performance enhancements, like using PostGIS for spatial indexing.
  - PostgreSQL offers strong querying performance, while the PostGIS extension helps us efficiently compute the K nearest vendors. (_While SQL performance is is well-suited for the current scale, see “What's Next” for discussion on a potential NoSQL alternative as the application grows._)

### Project Structure

- `api/` — Main backend server logic
  - `routes.py` — Defines API endpoints.
  - `errors.py` — Custom error handling.
  - `database/` — Database ORM models.
  - `models/` — Data models for API.
  - `service/` — Business logic and database query functions.
- `setup_scripts/` — Scripts for database initialization.
- `tests/` — Automated tests for configuration, integration, and database seeding.
- `config.py` — Application configuration.
- `requirements.txt` — Python dependencies.
- `Dockerfile` & `docker-compose.yml` — Backend and database containers.

## Immediate Code and Functionality Improvements

Code and functionality improvements we can make given more time.

### Keeping Data Updated

Currently, any updates to our source dataset [Mobile Food Facility Permit](https://data.sfgov.org/Economy-and-Community/Mobile-Food-Facility-Permit/rqzj-sfat/about_data) will not be propagated to our database. We will need to create a service to periodically update our database based on changes to the dataset. This can be done by comparing to the "last updated" timestamp available on the website (if provided) or by comparing every vendor.

**Trade-off**: this means that our database won't have the most up to date information. However, this isn't very crucial from a user experience perspective as this data isn't representative of anything time-sensitive, like live vendor location.

### Production

The project is currently configured to only run on development machines. We will need to configure it for production. This includes the following tasks:

- **Docker**: create production versions of `Docker`, `docker-compose.yml`, and `.env` files. We'll need to remove debug flags, avoid mounting our code to the container, host it on Gunicorn, etc.

- **Hosting**: find a provider like Heroku to host our backend and database

### Database Migration

As our project undergoes changes and project versioning, we will need to establish a method for migration our database schema. We should investigate using Alembic to track our database schema changes and manage schema upgrades of existing databases.

### Sorting and Improvements to Filtering

We need to provide sorting support. Currently, a frontend client will not be able to sort since our application enforces pagination. We will need to expose REST API query parameters for sorting.

## What's Next

### Scaling for More Users

Currently, this solution is not scalable to a large number of users querying our data. It is designed for a single server and database instance to handle all requests, which would quickly be bottlenecked by the server's hardware under heavy load.

To scale effectively, several improvements could be made:

- **Horizontal Backend Scaling:**
  Deploy multiple backend instances behind a load balancer to distribute incoming traffic. Cloud providers like AWS, GCP, or Azure make this relatively straightforward through managed services.

- **Database Scaling:**
  Horizontally scale the database (e.g. using a database like CockroachDB) to distribute its data across multiple database nodes.

### Migrating to NoSQL (Future Consideration)

Depending on future use cases, it may make sense to migrate certain components to a NoSQL datastore. SQL databases emphasize strong consistency (ACID compliance), which can come at the cost of performance and availability. For this application, real-time accuracy is not critical; eventual consistency would be acceptable.

However, if the workload remains primarily read-heavy with infrequent data updates, the advantages of switching to NoSQL would be limited, and PostgreSQL with PostGIS may continue to be the most practical choice.

### Scaling for Beyond San Francisco

We may eventually scale this application to all the food trucks around the world. In cases like this, we should critique the performance of our K nearest vendors search. Thanks to PostGIS and our spatial index (which uses bounding boxes to index / separate coordinates) we would only need to performance a distance comparison and sort with the vendors in the "vincinity" of the given coordinate. We would still face the problem of needing to horizontally scale our server and database, and utilize servers located near the geographic locations of potential users.

As the project expands to cover food trucks in other regions, or even globally, we would need to revisit the performance of the K-nearest vendors search.
Thanks to PostGIS and spatial indexing (which uses bounding boxes to efficiently narrow down nearby coordinates), only vendors within a given vicinity need to be compared and sorted by distance.
Still, scaling geographically would require horizontally scaling both the server and database, ideally deploying regional clusters close to end users to reduce latency.

### Authentication

We should secure our backend and implement some authentication mechanism with the frontend that will be making API requests.

## Running the Solution

> **_NOTE:_** run all of the following commands from the project root directory

#### Pre-requisites

- Docker and its CLI tools. See Docker's [Get Started](https://www.docker.com/get-started/) page to install Docker Desktop (which includes CLI).
- Python 3.12+

#### Running for the first time

1. Create your `.env` file with your configured environment variables. You can use the defaults in `.env.example` by simply running

   ```
   cp .env.example .env
   ```

2. Run the API

   ```
   docker compose up -d
   ```

3. Create database and populate with data

   ```
   docker compose run --rm backend python setup_scripts/db_init.py
   ```

4. Check the logs to make there are no errors

   ```
   # Backend logs
   docker logs -tf food_truck_lover_backend

   # Database logs
   docker logs -tf food_truck_lover_backend
   ```

5. The API is available at `http://localhost:8000`. You can check that it's running by accessing the API documentation:

   - http://localhost:8000/apidoc/redoc
   - http://localhost:8000/apidoc/swagger

#### Running tests

```
docker compose run --rm backend pytest
```

## API Endpoints

- `POST /vendors?page=...&page_size=...`

  - **Description:** Search for vendors by name, address, status, or location. Supports pagination.
  - **Request Body (JSON):**
    - `vendor_name` (string, optional): Case-insensitive partial match for vendor name.
    - `address` (string, optional): Case-insensitive partial match for address.
    - `status` (string, optional): Filter by application status (e.g., "APPROVED").
    - `locationFilter` (object, optional):
      - `location` (object):
        - `latitude` (float): Latitude coordinate.
        - `longitude` (float): Longitude coordinate.
      - `result_size` (integer): Number of nearest vendors to return (overrides pagination).
  - **Query Parameters:**
    - `page` (integer, required): Page number (1-based).
    - `page_size` (integer, required): Number of results per page.
  - **Response:** List of matching vendors.

**Notes:** this API allows users to search for vendors based on name, address, status, and location. They can query for a paginated list of vendors. If location filters are used, then pagination is ignored and `result_size` will be followed. Name, address, and status filters can still be used in conjunction with location filters. (In a future update, pagination query parameters and result_size should be merged. I don't see a reason to not use pagination when filtering by location.)

**Sample Request 1: Search by name and status (no location filter)**

```http
POST /vendors?page=1&page_size=10
Content-Type: application/json

{
  "vendor_name": "truly",
  "address": ""
  "status": "APPROVED"
}
```

**Sample Request 2: Search by location filter (nearest vendors)**

```http
POST /vendors?page=1&page_size=10
Content-Type: application/json

{
  "locationFilter": {
    "location": {
      "latitude": 37.7749,
      "longitude": -122.4194
    },
    "result_size": 5
  }
}
```
