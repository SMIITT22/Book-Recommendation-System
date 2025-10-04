# Book Recommendation System API

This project is a backend API for a simplified book recommendation system.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Setup and Run Instructions](#setup-and-run-instructions)
- [Architecture Explanation](#architecture-explanation)
- [How to Run Tests](#how-to-run-tests)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [API Usage](#api-usage)
- [Project Structure](#project-structure)

---

## 1. Project Overview

The API supports user authentication, listing books with dynamically calculated ratings, and a complete review and rating system. It is designed to be consumed by a frontend application. The implementation follows all core requirements of the case study, including a layered architecture, a reproducible Docker environment, and secure, asynchronous endpoints.

---

## 2. Setup and Run Instructions

Follow these instructions to get the project running on your local machine using Docker.

### Prerequisites

* Git  
* Docker and Docker Compose (Docker Desktop is recommended)

### Setup Steps

**A. Clone the Repository**

Open your terminal and clone the project from GitHub.

```bash
git clone https://github.com/SMIITT22/Book-Recommendation-System.git
cd Book-Recommendation-System
```

**B. Create the `.env` File**

Copy the example environment file to create your own local version:

```bash
# macOS / Linux
cp .env.example .env

# Windows
copy .env.example .env
```

Now you must manually set the following variables in the newly created `.env` file:

- `SECRET_KEY`
- `POSTGRES_PASSWORD`

To generate a secure `SECRET_KEY`, you can run this Python code:

```python
import secrets

# Generate a secure 32-byte random URL-safe key
secret_key = secrets.token_urlsafe(32)
print(secret_key)
```

You can run this on your local machine or use [https://www.online-python.com/](https://www.online-python.com/).

**Note:** If your `POSTGRES_PASSWORD` contains special characters, make sure to URL-encode it before inserting it into any connection string.

**C. Build and Run with Docker Compose**

This single command will build the Docker image, start the FastAPI app, and run the PostgreSQL container.

```bash
docker-compose up --build
```

The first time you run this, it may take a few minutes to download the base images and install all Python dependencies.

**D. Access the Application**

Once the containers are running successfully, the API will be available at:

```
http://localhost:8000
```

**API Root:**  
Open `http://localhost:8000/` in your browser. You should see the following response:

```json
{"status":"ok","message":"Welcome to the Book Recommendation System API!"}
```

**Interactive API Docs (Swagger UI):**  
The full interactive documentation, where you can test all endpoints, is available at:

```
http://localhost:8000/docs
```

---

## 3. Architecture Explanation

This project follows a clean, layered architecture to ensure a strong separation of concerns, making the codebase maintainable and testable.

**API Layer (app/api/):**  
Contains the FastAPI routers and endpoints. It handles all HTTP request/response logic and data validation.

**Service Layer (app/services/):**  
Contains all the business logic, such as calculating average ratings or deciding whether to create or update a review.

**Repository Layer (app/repositories/):**  
Responsible for all database interactions. It contains functions that execute specific database queries using SQLAlchemy.

**Core & Schemas:**

- `app/core/`: Manages central services like database connections, configuration, and security dependencies.  
- `app/schemas/`: Contains all Pydantic models used for API validation and data transfer.

Each layer is isolated and communicates only with adjacent layers, and dependencies are injected to allow for easy mocking in tests.

---

## 4. How to Run Tests

The project includes a suite of integration tests that verify the service layer logic while mocking the repository layer, as required by the case study.

**Step 1: Ensure the Application is Running**

First, make sure your Docker containers are up and running.

```bash
docker-compose up
```

**Step 2: Execute the Test Suite**

In a separate terminal, run the following command. This will execute the pytest command inside the running web container.

```bash
docker-compose exec web pytest
```

**Expected Output:**

You will see the test results in your terminal, concluding with a summary indicating that all tests have passed.

```
============================= 3 passed in X.XXs ==============================
```

---

## 5. Features

**User Authentication:**  
Secure login endpoint (`/api/v1/auth/login`) that returns a JWT token. User data is managed in-memory, initialized from a `users.json` file.

**Book Listings:**  
A protected endpoint (`/api/v1/books/`) to list all books. Supports searching by title/author and pagination (`skip`/`limit`).

**Dynamic Ratings:**  
Each book's average rating is dynamically calculated from user reviews stored in the database.

**Review System:**
- `POST /api/v1/books/{book_id}/reviews`: Add or update a review (rating 1–5 and text).  
- `GET /api/v1/books/{book_id}/reviews`: Fetch all reviews for a book.

---

## 6. Tech Stack

- **Language:** Python 3.11  
- **Framework:** FastAPI  
- **Database:** PostgreSQL (via Docker)  
- **ORM:** SQLAlchemy  
- **Authentication:** JWT + passlib (bcrypt)  
- **Validation:** Pydantic  
- **Async Support:** Fully asynchronous endpoints and database interactions  
- **Containerization:** Docker & Docker Compose

---

## 7. API Usage

Most endpoints require authentication using a JWT token.

**Available users (from `users.json`):**
- Username: `smitpatel2002` — Password: `smit123`
- Username: `arthurmorgan2018` — Password: `arthur123`

**Authentication via Swagger UI:**
1. Open `http://localhost:8000/docs`.
2. Click the green **Authorize** button.
3. In the dialog, enter a username and password (listed above). The Token URL is `/api/v1/auth/login` and the flow is `password`.
4. Click **Authorize** in the dialog. Swagger UI will obtain an access token and store it for you.
5. After authorizing once, the token is automatically attached to subsequent requests for endpoints that require JWT authentication. You do not need to manually add the `Authorization: Bearer <token>` header for each call.

**Alternative (Postman):**
1. Send a `POST` request to `/api/v1/auth/login` with body:
   ```json
   {
     "username": "smitpatel2002",
     "password": "smit123"
   }
   ```
2. Copy the `access_token` from the response.
3. For protected endpoints, set the header:
   ```
   Authorization: Bearer <access_token>
   ```

---

## 8. Project Structure

```
book-recommendation-system/
├── app/
│   ├── api/            # FastAPI routers
│   ├── core/           # Configs, DB, security
│   ├── models/         # SQLAlchemy ORM models
│   ├── repositories/   # Data access layer
│   ├── schemas/        # Pydantic models
│   └── services/       # Business logic
├── tests/              # Pytest test suite
├── books.json          # Book data for seeding
├── users.json          # In-memory user seed file
├── .env.example        # Sample environment file
├── docker-compose.yml  # Docker config
└── README.md           # This file
```
