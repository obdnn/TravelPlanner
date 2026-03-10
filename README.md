# Travel Planner API

## Overview
This is a CRUD application built with Django REST Framework (DRF) that helps travelers plan trips and collect desired places to visit. It integrates with the public **Art Institute of Chicago API** to validate and fetch place data.

## Features Implemented
* **Travel Projects:** Create, list, retrieve, update, and delete travel projects.
* **Project Places:** Import places from a third-party API directly when creating a project.
* **Business Logic & Validations:**
  * Validates that a place exists in the Art Institute API before adding it.
  * Enforces a limit of a maximum of 10 places per project.
  * Prevents adding the exact same external place to the same project.
  * A project cannot be deleted if any of its places are already marked as visited.
  * A project is dynamically marked as `is_completed` when all its places are visited.

## Tech Stack
* Python 3.13
* Django & Django REST Framework
* MySQL 
* `requests` (for third-party API integration)

## Environment Variables
Create a `.env` file in the root directory and add the following variables:

```env
SECRET_KEY=your_secret_key_here
DEBUG=True

# Database configurations (if using MySQL)
DB_NAME=travelplanner
DB_USER=your
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone <https://github.com/obdnn/TravelPlanner>
   cd travel_planner
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server:**
   ```bash
   python manage.py runserver
   ```
## API Documentation (Swagger / OpenAPI)
Interactive API documentation is provided via Swagger UI using `drf-spectacular`. 

Once the server is running, you can explore and test all endpoints, validations, and use cases directly in your browser without needing any external tools.

* **Swagger UI:** `http://127.0.0.1:8000/api/docs/`
* **OpenAPI Schema:** `http://127.0.0.1:8000/api/schema/`

Alternatively, the base URL for the API is `http://127.0.0.1:8000/api/`.

### Example Request (Create Project with Places)
### 1. Create a Project with Places
**POST** `http://127.0.0.1:8000/api/projects/`
```json
{
    "name": "Trip to Chicago",
    "description": "Art tour",
    "places": [
        {"external_id": "27992", "notes": "Must see!"}
    ]
}
```

### 2. List All Projects
**GET** `http://127.0.0.1:8000/api/projects/`
Returns an array of all travel projects, including their nested places and the dynamically calculated `is_completed` status.

### 3. Update a Place (Mark as Visited & Edit Notes)
**PATCH** `http://127.0.0.1:8000/api/places/1/`
```json
{
    "notes": "It was amazing, highly recommend!",
    "is_visited": true
}
```

### 4. Delete a Project
**DELETE** `http://127.0.0.1:8000/api/projects/1/`
*(Note: As per business requirements, this will return a `400 Bad Request` if any places within the project are already marked as visited).*
