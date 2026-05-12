# Last Mile Logistics — Backend Documentation

## Overview

A REST API built with **Flask** and **PostgreSQL** for managing last-mile delivery operations. It handles four core resources: drivers, vehicles, routes, and packages. Flask also serves the compiled React frontend as static files, making it the single entry point for the full application.

---

## Tech Stack

| Layer        | Technology                          |
|--------------|-------------------------------------|
| Framework    | Flask 3.1.3                         |
| CORS         | Flask-Cors 5.0.0                    |
| Database     | PostgreSQL (via psycopg2-binary 2.9.12) |
| Config       | python-dotenv 1.2.2                 |
| Frontend     | React 18 (served as static build)   |
| Runtime      | Python 3.x                          |

---

## Project Structure

```
last-mile_logistics/
├── app.py              # Flask app — API routes + serves React
├── database.py         # DB connection, schema init, CRUD functions
├── requirements.txt
├── .env                # Environment variables (not committed)
├── templates/
│   └── index.html      # React build entry point
├── static/
│   └── assets/         # React JS and CSS bundles
├── venv/               # Python virtual environment (not committed)
└── public/
    └── last-mile_ERD.png
```

---

## Environment Setup

Create a `.env` file in the project root:

```env
DB_HOST=your_host
DB_PORT=5432
DB_NAME=your_database
DB_USER=your_user
DB_PASS=your_password
```

Create and activate the virtual environment:

```bash
python -m venv venv
.\venv\Scripts\activate        # Windows
source venv/bin/activate       # Mac/Linux
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the server:

```bash
python app.py
```

The server starts on `http://0.0.0.0:5000`. On startup, `init_db()` creates the schema and all tables if they don't already exist. The React UI is served at `http://localhost:5000`.

---

## Serving the React Frontend

The React app is built separately (`npm run build` in the frontend project) and the output is copied into Flask:

- `dist/index.html` → `templates/index.html`
- `dist/assets/` → `static/assets/`

Flask serves `index.html` for all non-API routes via a catch-all route, enabling React Router to handle client-side navigation.

---

## Database Schema

All tables live under the `lmlogistics` schema in PostgreSQL.

### `lmlogistics.driver`

| Column         | Type         | Notes       |
|----------------|--------------|-------------|
| `driver_id`    | serial       | Primary key |
| `name`         | varchar(100) |             |
| `license_type` | varchar(50)  |             |

### `lmlogistics.vehicle`

| Column          | Type        | Notes                                      |
|-----------------|-------------|--------------------------------------------|
| `vehicle_id`    | serial      | Primary key                                |
| `license_plate` | varchar(20) | Unique                                     |
| `model`         | varchar(50) |                                            |
| `driver_id`     | int         | Unique — FK → `driver.driver_id` (1-to-1) |

### `lmlogistics.route`

| Column         | Type         | Notes                   |
|----------------|--------------|-------------------------|
| `route_id`     | serial       | Primary key             |
| `date`         | date         |                         |
| `service_zone` | varchar(100) |                         |
| `driver_id`    | int          | FK → `driver.driver_id` |

### `lmlogistics.package`

| Column        | Type          | Notes                 |
|---------------|---------------|-----------------------|
| `package_id`  | serial        | Primary key           |
| `description` | varchar(250)  |                       |
| `weight`      | decimal(10,2) | Must be > 0           |
| `route_id`    | int           | FK → `route.route_id` |

---

## API Reference

Base URL: `http://localhost:5000`

All request bodies use `Content-Type: application/json`. All responses return JSON.

---

### Health Check

#### `GET /api`

Returns a status message confirming the API is running.

**Response**
```json
{ "message": "Last Mile Logistics Online" }
```

---

### Drivers

#### `GET /drivers`
Returns all drivers.

**Response** `200 OK`
```json
[{ "driver_id": 1, "name": "Jane Doe", "license_type": "CDL-A" }]
```

#### `POST /drivers`
Creates a new driver.

**Request Body**
```json
{ "name": "Jane Doe", "license_type": "CDL-A" }
```
**Response** `200 OK`
```json
{ "message": "Driver Created" }
```

#### `PUT /drivers/<driver_id>`
Updates an existing driver's name and license type.

**Request Body**
```json
{ "name": "Jane Doe", "license_type": "CDL-B" }
```
**Response** `200 OK`
```json
{ "message": "Driver updated successfully" }
```

#### `DELETE /drivers/<driver_id>`
Deletes a driver by ID.

**Response** `200 OK`
```json
{ "message": "Driver deleted successfully" }
```

---

### Vehicles

#### `GET /vehicles`
Returns all vehicles.

**Response** `200 OK`
```json
[{ "vehicle_id": 1, "license_plate": "ABC-1234", "model": "Ford Transit", "driver_id": 1 }]
```

#### `POST /vehicles`
Creates a new vehicle. Each driver can only be assigned one vehicle (`driver_id` is unique).

**Request Body**
```json
{ "license_plate": "ABC-1234", "model": "Ford Transit", "driver_id": 1 }
```
**Response** `200 OK`
```json
{ "message": "Vehicle added" }
```

#### `PUT /vehicles/<vehicle_id>`
Updates a vehicle's license plate and model. Driver assignment cannot be changed via this endpoint.

**Request Body**
```json
{ "license_plate": "XYZ-9999", "model": "Mercedes Sprinter" }
```
**Response** `200 OK`
```json
{ "message": "Vehicle updated successfully" }
```

#### `DELETE /vehicles/<vehicle_id>`
Deletes a vehicle by ID.

**Response** `200 OK`
```json
{ "message": "Vehicle deleted successfully" }
```

---

### Routes

#### `GET /routes`
Returns all routes.

**Response** `200 OK`
```json
[{ "route_id": 1, "date": "2026-05-07", "service_zone": "Zone A", "driver_id": 1 }]
```

#### `POST /routes`
Creates a new delivery route.

**Request Body**
```json
{ "date": "2026-05-07", "service_zone": "Zone A", "driver_id": 1 }
```
**Response** `200 OK`
```json
{ "message": "Routed added" }
```

#### `PUT /routes/<route_id>`
Updates a route's service zone.

**Request Body**
```json
{ "service_zone": "Zone B — Uptown" }
```
**Response** `200 OK`
```json
{ "message": "Route updated successfully" }
```

#### `DELETE /routes/<route_id>`
Deletes a route by ID. Any packages linked to this route must be deleted first (FK constraint).

**Response** `200 OK`
```json
{ "message": "Route deleted successfully" }
```

---

### Packages

#### `GET /packages`
Returns all packages.

**Response** `200 OK`
```json
[{ "package_id": 1, "description": "Electronics", "weight": 2.50, "route_id": 1 }]
```

#### `POST /packages`
Adds a package to a route.

**Request Body**
```json
{ "description": "Electronics", "weight": 2.50, "route_id": 1 }
```
**Response** `200 OK`
```json
{ "message": "Package added" }
```

#### `PUT /packages/<package_id>`
Updates a package's description and weight.

**Request Body**
```json
{ "description": "Fragile glassware", "weight": 1.20 }
```
**Response** `200 OK`
```json
{ "message": "Package updated successfully" }
```

#### `DELETE /packages/<package_id>`
Deletes a package by ID.

**Response** `200 OK`
```json
{ "message": "Package deleted successfully" }
```

---

## Database Module (`database.py`)

| Function                                              | Description                                          |
|-------------------------------------------------------|------------------------------------------------------|
| `get_connection()`                                    | Opens and returns a psycopg2 connection using env vars |
| `init_db()`                                           | Creates schema and all four tables if they don't exist |
| `create_driver(name, license_type)`                   | Inserts a new driver record                          |
| `get_drivers()`                                       | Returns all driver rows as dicts                     |
| `update_driver(driver_id, name, license_type)`        | Updates name and license type for a driver           |
| `delete_driver(driver_id)`                            | Deletes a driver by ID                               |
| `create_vehicle(license_plate, model, driver_id)`     | Inserts a new vehicle record                         |
| `get_vehicles()`                                      | Returns all vehicle rows as dicts                    |
| `update_vehicle(vehicle_id, license_plate, model)`    | Updates license plate and model for a vehicle        |
| `delete_vehicle(vehicle_id)`                          | Deletes a vehicle by ID                              |
| `create_route(date, service_zone, driver_id)`         | Inserts a new route record                           |
| `get_routes()`                                        | Returns all route rows as dicts                      |
| `update_route(route_id, service_zone)`                | Updates the service zone for a route                 |
| `delete_route(route_id)`                              | Deletes a route by ID                                |
| `create_package(description, weight, route_id)`       | Inserts a new package record                         |
| `get_packages()`                                      | Returns all package rows as dicts                    |
| `update_package(package_id, description, weight)`     | Updates description and weight for a package         |
| `delete_package(package_id)`                          | Deletes a package by ID                              |

All functions open a new connection, execute their query, commit if writing, then close the connection. `RealDictCursor` is used on reads so rows come back as dictionaries rather than tuples.

---

## Notes for Developers

- **No connection pooling** — each function opens and closes its own connection. For production, consider `psycopg2.pool` or `SQLAlchemy`.
- **No input validation** — the API will raise a `KeyError` if required fields are missing. Adding `marshmallow` or `pydantic` is recommended before production.
- **Debug mode is on** — disable `debug=True` in `app.run()` before deploying.
- **Schema creation** — `init_db()` runs `CREATE SCHEMA IF NOT EXISTS lmlogistics` automatically on startup.
- **Frontend rebuild** — after any React changes, run `npm run build` in the frontend project and re-copy `dist/index.html` → `templates/` and `dist/assets/` → `static/assets/`.
