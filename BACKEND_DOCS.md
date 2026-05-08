# Last Mile Logistics — Backend Documentation

## Overview

A REST API built with **Flask** and **PostgreSQL** for managing last-mile delivery operations. It handles four core resources: drivers, vehicles, routes, and packages.

---

## Tech Stack

| Layer      | Technology              |
|------------|-------------------------|
| Framework  | Flask 3.1.3             |
| Database   | PostgreSQL (via psycopg2-binary 2.9.12) |
| Config     | python-dotenv 1.2.2     |
| Runtime    | Python 3.x              |

---

## Project Structure

```
last-mile_logistics/
├── app.py          # Flask app, route definitions
├── database.py     # DB connection, schema init, CRUD functions
├── requirements.txt
├── .env            # Environment variables (not committed)
└── public/
    └── last-mile_ERD.png
```

---

## Environment Setup

Create a `.env` file in the project root with the following variables:

```env
DB_HOST=your_host
DB_PORT=5432
DB_NAME=your_database
DB_USER=your_user
DB_PASS=your_password
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the server:

```bash
python app.py
```

The server starts on `http://0.0.0.0:5000` with debug mode enabled. On startup, `init_db()` is called automatically to create all tables if they don't already exist.

---

## Database Schema

All tables live under the `lmlogistics` schema in PostgreSQL.

### `lmlogistics.driver`

| Column        | Type          | Notes                  |
|---------------|---------------|------------------------|
| `driver_id`   | serial        | Primary key            |
| `name`        | varchar(100)  |                        |
| `license_type`| varchar(50)   |                        |

### `lmlogistics.vehicle`

| Column          | Type         | Notes                                      |
|-----------------|--------------|--------------------------------------------|
| `vehicle_id`    | serial       | Primary key                                |
| `license_plate` | varchar(20)  | Unique                                     |
| `model`         | varchar(50)  |                                            |
| `driver_id`     | int          | Unique — FK → `driver.driver_id` (1-to-1) |

### `lmlogistics.route`

| Column         | Type          | Notes                        |
|----------------|---------------|------------------------------|
| `route_id`     | serial        | Primary key                  |
| `date`         | date          |                              |
| `service_zone` | varchar(100)  |                              |
| `driver_id`    | int           | FK → `driver.driver_id`      |

### `lmlogistics.package`

| Column        | Type           | Notes                          |
|---------------|----------------|--------------------------------|
| `package_id`  | serial         | Primary key                    |
| `description` | varchar(250)   |                                |
| `weight`      | decimal(10,2)  | Must be > 0                    |
| `route_id`    | int            | FK → `route.route_id`          |

---

## API Reference

Base URL: `http://localhost:5000`

All request bodies use `Content-Type: application/json`. All responses return JSON.

---

### Health Check

#### `GET /`

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
[
  { "driver_id": 1, "name": "Jane Doe", "license_type": "CDL-A" }
]
```

---

#### `POST /drivers`

Creates a new driver.

**Request Body**
```json
{
  "name": "Jane Doe",
  "license_type": "CDL-A"
}
```

**Response** `200 OK`
```json
{ "message": "Driver Created" }
```

---

### Vehicles

#### `GET /vehicles`

Returns all vehicles.

**Response** `200 OK`
```json
[
  { "vehicle_id": 1, "license_plate": "ABC-1234", "model": "Ford Transit", "driver_id": 1 }
]
```

---

#### `POST /vehicles`

Creates a new vehicle and assigns it to a driver. Each driver can only be assigned one vehicle (`driver_id` is unique).

**Request Body**
```json
{
  "license_plate": "ABC-1234",
  "model": "Ford Transit",
  "driver_id": 1
}
```

**Response** `200 OK`
```json
{ "message": "Vehicle added" }
```

---

### Routes

#### `GET /routes`

Returns all routes.

**Response** `200 OK`
```json
[
  { "route_id": 1, "date": "2026-05-07", "service_zone": "Zone A", "driver_id": 1 }
]
```

---

#### `POST /routes`

Creates a new delivery route.

**Request Body**
```json
{
  "date": "2026-05-07",
  "service_zone": "Zone A",
  "driver_id": 1
}
```

**Response** `200 OK`
```json
{ "message": "Routed added" }
```

---

### Packages

#### `GET /packages`

Returns all packages.

**Response** `200 OK`
```json
[
  { "package_id": 1, "description": "Electronics", "weight": 2.50, "route_id": 1 }
]
```

---

#### `POST /packages`

Adds a package to a route.

**Request Body**
```json
{
  "description": "Electronics",
  "weight": 2.50,
  "route_id": 1
}
```

**Response** `200 OK`
```json
{ "message": "Package added" }
```

---

## Database Module (`database.py`)

| Function                                          | Description                                      |
|---------------------------------------------------|--------------------------------------------------|
| `get_connection()`                                | Opens and returns a psycopg2 connection using env vars |
| `init_db()`                                       | Creates all four tables if they don't exist      |
| `create_driver(name, license_type)`               | Inserts a new driver record                      |
| `get_drivers()`                                   | Returns all driver rows as dicts                 |
| `create_vehicle(license_plate, model, driver_id)` | Inserts a new vehicle record                     |
| `get_vehicles()`                                  | Returns all vehicle rows as dicts                |
| `create_route(date, service_zone, driver_id)`     | Inserts a new route record                       |
| `get_routes()`                                    | Returns all route rows as dicts                  |
| `create_package(description, weight, route_id)`   | Inserts a new package record                     |
| `get_packages()`                                  | Returns all package rows as dicts                |

All functions open a new connection, execute their query, commit if writing, then close the connection. `RealDictCursor` is used on reads so rows come back as dictionaries rather than tuples.

---

## Notes for Developers

- **No connection pooling** — each function opens and closes its own connection. For production, consider using a pool (e.g., `psycopg2.pool` or `SQLAlchemy`).
- **No input validation** — the API will raise a `KeyError` if required fields are missing from the request body. Adding validation middleware (e.g., `marshmallow` or `pydantic`) is recommended before going to production.
- **Debug mode is on** — `debug=True` is set in `app.run()`. Disable this in production.
- **Schema creation** — `init_db()` runs `CREATE SCHEMA IF NOT EXISTS lmlogistics` automatically before creating tables, so no manual setup is needed.
