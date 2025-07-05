# Django Expense Tracker API

A RESTful API for tracking personal expenses and income with user authentication, built with Django and Django REST Framework.

## Core Features

- **User Authentication**: Secure user registration and login using JWT (JSON Web Tokens).
- **Data Isolation**: Regular users can only access and manage their own records.
- **Admin Access**: Superusers have full access to manage all users' records.
- **CRUD Operations**: Full Create, Read, Update, and Delete functionality for expense/income records.
- **Automatic Tax Calculation**: Supports both flat and percentage-based tax calculations.
- **Pagination**: API responses for lists are paginated for efficiency.

## Setup and Installation

1.  **Clone the repository:**

    ```bash
    git clone <your-repo-url>
    cd expense_tracker
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply database migrations:**

    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser to manage the application:**

    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The API will be available at `http://127.0.0.1:8000/`.

## API Endpoints

All endpoints are prefixed with `/api/`. Authentication is required for all `/expenses/` endpoints.

### Authentication

| Method | Endpoint          | Description                                  |
| :----- | :---------------- | :------------------------------------------- |
| `POST` | `/auth/register/` | Register a new user.                         |
| `POST` | `/auth/login/`    | Log in to get JWT access and refresh tokens. |
| `POST` | `/auth/refresh/`  | Refresh an expired access token.             |

### Expense/Income Records

| Method   | Endpoint          | Description                            |
| :------- | :---------------- | :------------------------------------- |
| `GET`    | `/expenses/`      | List all of your records (paginated).  |
| `POST`   | `/expenses/`      | Create a new expense or income record. |
| `GET`    | `/expenses/{id}/` | Retrieve a specific record by its ID.  |
| `PUT`    | `/expenses/{id}/` | Fully update a specific record.        |
| `PATCH`  | `/expenses/{id}/` | Partially update a specific record.    |
| `DELETE` | `/expenses/{id}/` | Delete a specific record.              |

### Sample Requests

**1. Register a new user:**

curl -X POST http://127.0.0.1:8000/api/auth/register/ \
-H "Content-Type: application/json" \
-d '{
"username": "newuser",
"email": "new@example.com",
"password": "strongpassword123"
}'

**2. Login to get tokens:**

curl -X POST http://127.0.0.1:8000/api/auth/login/ \
-H "Content-Type: application/json" \
-d '{
"username": "newuser",
"password": "strongpassword123"
}'

**3. Create a new expense (with token):**

curl -X POST http://127.0.0.1:8000/api/expenses/ \
-H "Authorization: Bearer <your_access_token>" \
-H "Content-Type: application/json" \
-d '{
"title": "Monthly Rent",
"amount": "1200.00",
"transaction_type": "debit",
"tax": "0",
"tax_type": "flat"
}'

**4. List all your expenses (with token):**

curl -X GET http://127.0.0.1:8000/api/expenses/ \
-H "Authorization: Bearer <your_access_token>"
