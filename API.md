# FeastForward API Reference

This document describes the routes currently implemented in `backend.py.py`. Start the Flask server from the repository root:

```bash
python backend.py.py
```

The local API listens on `http://127.0.0.1:5000` by default. Send JSON requests with the `Content-Type: application/json` header.

## Routes

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/` | Basic service status |
| POST | `/register` | Register a provider, volunteer, or recipient |
| POST | `/food` | Create a food donation post |
| GET | `/food` | List food posts (available by default) |
| POST | `/volunteer` | Create a volunteer profile for an existing volunteer user |
| POST | `/recipient` | Create a recipient profile for an existing recipient user |

## Register a user

```json
{
  "name": "Community Kitchen",
  "email": "kitchen@example.org",
  "password": "replace-with-a-strong-password",
  "role": "provider",
  "location": "Chennai"
}
```

Allowed roles are `provider`, `volunteer`, and `recipient`. Passwords must contain at least eight characters and are stored as password hashes. The current prototype does not implement a login or token-based authorization route.

## Create a food post

```json
{
  "provider_id": 1,
  "type": "Prepared meals",
  "quantity": 25,
  "freshness_score": 0.9,
  "location": "Chennai"
}
```

The provider ID must belong to an existing user whose role is `provider`. Quantity must be a positive integer. Freshness score is optional and, when supplied, must be between 0 and 1.

## List food posts

```http
GET /food
GET /food?status=available
```

Supported status filters are `available`, `picked up`, and `delivered`.

## Create volunteer and recipient profiles

A volunteer profile requires an existing volunteer user's ID:

```json
{
  "user_id": 2,
  "vehicle_type": "Bicycle"
}
```

A recipient profile requires an existing recipient user's ID and a positive number of people:

```json
{
  "user_id": 3,
  "food_requirements": "Vegetarian meals",
  "number_of_people": 40
}
```

## Error handling

The API returns JSON error messages for invalid JSON bodies and invalid field values. Duplicate unique email values or database integrity errors return HTTP 409. Missing or wrong-role user references return HTTP 404.

## Prototype limitations

- There is no authentication/session flow yet; do not expose this API publicly with real personal data.
- CORS is currently configured broadly and should be restricted to trusted frontend origins before deployment.
- Food matching, freshness verification, volunteer dispatch, live tracking, and notifications are not implemented by these routes.
- The freshness score is a caller-provided value, not an AI food-safety assessment. Never use it to establish that food is safe to consume.
