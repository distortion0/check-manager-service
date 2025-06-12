# FastAPI Checks App

A check management API built with FastAPI, PostgreSQL, and Docker.  
Features include user registration and login with JWT authentication, 
creating and filtering receipts (checks), and viewing receipt 
details. (public view as well)

---

## Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker & Docker Compose

---

## How to install and run

### Setup and Run with Docker

1. Clone the repo:  
   ```bash
   git clone <repo-url>
   cd <repo-folder>
   ```
2. Create a .env file and configure environment variables 
(see .env.example for reference)

3. Build and start containers:

    ```bash
    docker-compose up --build
    ```
   Access the API docs at http://localhost:8000/docs

---
## Endpoints

### Authentication
- POST /register
  - 
Register a new user.
Request Body:

```json
{
  "username": "string",
  "password": "string",
  "full_name": "string"
}
```
Response: Created user details (including hashed password).

- POST /login
  - 
Login and get JWT access token.
Form Data:

   - username: string
   - password: string

Response:

```json
{
  "access_token": "jwt_token",
  "token_type": "bearer"
}
```
### Checks (Receipts)

**All endpoints below (except the public one) require Bearer token authentication.**

- POST /checks/
  - 
Create a new check.
Request Body:

```json
{
  "payment": {
    "type": "string",
    "amount": float
  },
  "products": [
    {
      "name": "string",
      "price": float,
      "quantity": float
    }
  ],
  "additional_data": "string (optional)"
}
```
Response: Created check details.

- GET /checks/
  - 
Get a list of checks for the current user with optional filters and pagination.
Query Parameters:

      date_from: ISO date string (optional)
      date_to: ISO date string (optional)
      min_total: float (optional)
      payment_type: string (optional)
      offset: integer (default 0)
      limit: integer (default 10)

Response: List of checks with summary info.

- GET /checks/{check_id}
  - 
Get details of a specific check by ID.
Path Parameter:

      check_id: integer

Response: Full check details including products.

- GET /checks/public/{token}
  - 
Public text view of a check by its public token (no authentication required).
Path Parameter:

      token: string

Query Parameters:

      line_width: integer (default 32, min 10, max 80) — sets text formatting width

Response: Plain text receipt content.

---

**Testing environment is available in SWAGGER http://localhost:8000/docs, 
Oauth requires only login and password, then it manager bearer token automatically**