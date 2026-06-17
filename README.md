# Last Mile Logistics

A full-stack delivery management app built with **Flask**, **PostgreSQL**, and **React**. Flask serves both the REST API and the compiled React frontend from a single server.

---

## Quick Start

```bash
python -m venv venv
.\venv\Scripts\activate          # Windows (use source venv/bin/activate on Mac/Linux)
pip install -r requirements.txt
```

Create a `.env` file:

```env
DB_HOST=your_host
DB_PORT=5432
DB_NAME=your_database
DB_USER=your_user
DB_PASS=your_password
```

Run:

```bash
python app.py
```

App starts at `http://localhost:5000`. Tables are created automatically on first run.

---

## What It Does

Full CRUD for four resources:

- **Drivers** — name, license type
- **Vehicles** — license plate, model, assigned driver (1:1)
- **Routes** — date, service zone, assigned driver
- **Packages** — description, weight, assigned route

---

## API

16 REST endpoints across `/drivers`, `/vehicles`, `/routes`, and `/packages` (GET, POST, PUT, DELETE for each). See [BACKEND_DOCS.md](BACKEND_DOCS.md) for full details.

---

## Tech Stack

Flask 3.1.3 · PostgreSQL (psycopg2) · React 18 · python-dotenv

---

## Notes

- No connection pooling or input validation — not production-ready as-is.
- To rebuild the frontend: run `npm run build` in the React project, then copy `dist/index.html` → `templates/` and `dist/assets/` → `static/assets/`.
