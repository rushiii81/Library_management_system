# Library Management System (Django REST Framework)

## Features
- Admin can Add, Edit, and Delete books.
- Students can only view books.
- Token-based authentication.
- CRUD operations for books.
- Secure API with DRF permissions.

## Setup Instructions
1. **Clone the repository**  

https://github.com/rahulkale12/Library-management-system-DRF-.git


2. **Create and activate a virtual environment**  

python -m venv venv source venv/bin/activate


3. **Install dependencies**  

pip install -r requirements.txt


4. **Run migrations**  

python manage.py makemigrations python manage.py migrate


5. **Create a superuser**  

python manage.py createsuperuser


6. **Run the server**  

python manage.py runserver



## API Endpoints
- `GET /api/books/` → View all books (Students & Admins)
- `POST /api/books/` → Add a book (Admins only)
- `PUT /api/books/<id>/` → Edit a book (Admins only)
- `DELETE /api/books/<id>/` → Delete a book (Admins only)

## Authentication
- Login via token authentication.
- Use the token in API requests.


