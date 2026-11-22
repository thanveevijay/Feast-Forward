# FeastForward — Rescue Food. Feed Lives.

FeastForward is a food-rescue prototype that connects surplus-food providers with organizations that can distribute food to people in need. The current repository contains a Flask API backed by SQLite and a basic frontend.

## Current backend capabilities

The Flask application currently provides these endpoints:

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/` | Backend health/welcome response |
| POST | `/register` | Register a user |
| POST | `/food` | Create a food donation post |
| GET | `/food` | List food donation posts |
| POST | `/volunteer` | Register a volunteer profile |
| POST | `/recipient` | Register a recipient profile |

Requests that create records should use a JSON body with the fields required by the corresponding model.

### Example: create a food post

```json
{
  "provider_id": 1,
  "type": "Prepared meals",
  "quantity": 25,
  "freshness_score": 0.9,
  "location": "Chennai"
}
```

Send this body to `POST /food` with the `Content-Type: application/json` header. The `provider_id` must refer to an existing user.

## Technology

- **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-CORS
- **Database:** SQLite
- **Frontend:** frontend source is maintained in the `frontend/` directory

## Run locally

1. Install Python 3.10 or later.
2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   # Windows PowerShell
   .venv\Scripts\Activate.ps1
   # macOS / Linux
   source .venv/bin/activate
   ```

3. Install backend dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the API from the repository root:

   ```bash
   python backend.py.py
   ```

5. Open `http://127.0.0.1:5000/`. The SQLite database is created automatically when the application starts.

## Important security and implementation notes

This repository is an early-stage prototype, not a production-ready food-distribution service. In particular:

- Registration hashes passwords with Werkzeug before storing them. The prototype does not yet expose a login/token-authentication flow, so protected user sessions and authorization are not implemented.
- The API currently enables CORS broadly. Restrict allowed origins before deployment; debug mode is disabled when the server is run directly.
- The current backend exposes basic user, food, volunteer, and recipient records. AI matching, live delivery tracking, food-safety verification, and notification workflows are product goals, not capabilities implemented by the current Flask file.
- Validate all input, handle duplicate emails and missing records, and add automated tests before using real data.

## Project goal

The long-term goal is to reduce avoidable food waste by making it easier for surplus-food providers, recipient organizations, and volunteers to coordinate safe and timely food redistribution.
