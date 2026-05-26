# 📚 Library Management API

A RESTful API for managing a library system, built with **FastAPI**, **SQLAlchemy**, and **Alembic**.  
It allows you to manage users, authors, books, and borrowing/returning operations with full database migration support.

## ✨ Features

- User management (create, list, retrieve)
- Author management (create, list, retrieve)
- Book management (create, list, retrieve, update available copies)
- Borrow & return books with automatic copy count adjustment
- Active borrow records tracking
- Race condition prevention using `SELECT ... FOR UPDATE` on borrowing
- Custom exceptions for clear error handling (404 / 400)
- Database migrations with Alembic
- Environment variables for sensitive data (`.env`)
- Automatic API documentation (Swagger UI & ReDoc)

## 🛠️ Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) – Web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) – ORM
- [Alembic](https://alembic.sqlalchemy.org/) – Database migrations
- [PyMySQL](https://pymysql.readthedocs.io/) – MySQL driver
- [Pydantic](https://docs.pydantic.dev/) – Data validation
- [python-dotenv](https://github.com/theskumar/python-dotenv) – Environment variables

## 📁 Project Structure
.
├── app/
│ ├── init.py
│ ├── main.py # FastAPI app & endpoints
│ ├── models.py # SQLAlchemy models
│ ├── schemas.py # Pydantic schemas
│ ├── crud.py # CRUD operations
│ ├── db.py # Database engine & session
│ ├── settings.py # Load .env variables
│ └── migrations/ # Alembic migrations
├── .env # Environment variables (ignored by git)
├── .gitignore
├── alembic.ini
├── requirements.txt
└── README.md

---

## 🚀 Getting Started

### 1️⃣ Clone the repository

git clone https://github.com/your-username/library-management-fastapi.git
cd library-management-fastapi

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

pip install -r requirements.txt
alembic upgrade head

uvicorn app.main:app --reload

The API will be available at `http://localhost:8000`

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 📌 API Endpoints

| Method | Endpoint                      | Description                         |
|--------|-------------------------------|-------------------------------------|
| POST   | `/users/`                     | Create a new user                   |
| GET    | `/users/`                     | List all users                      |
| GET    | `/users/{user_id}`            | Get user by ID                      |
| POST   | `/authors/`                   | Create a new author                 |
| GET    | `/authors/`                   | List all authors                    |
| GET    | `/authors/{author_id}`        | Get author by ID                    |
| POST   | `/books/`                     | Create a new book                   |
| GET    | `/books/`                     | List all books                      |
| GET    | `/books/{book_id}`            | Get book by ID                      |
| PUT    | `/books/{book_id}/copies`     | Update available copies             |
| POST   | `/borrow/`                    | Borrow a book                       |
| POST   | `/return/{borrow_id}`         | Return a borrowed book              |
| GET    | `/borrow/user/{user_id}`      | Get all borrows of a user           |
| GET    | `/borrow/active/`             | List all active borrows             |

## ⚠️ Error Handling

The API returns appropriate HTTP status codes with descriptive messages:

- `400` – Validation error or business logic violation (e.g., no copies left, already returned)
- `404` – Resource not found (user, book, author, borrow record)
- `500` – Internal server error (should not happen under normal conditions)

## 👤 Author

**Your Name**  
[zinebgr]  
[zinebgrabsi.gmail.com]

## 🙏 Acknowledgements

- FastAPI documentation
- SQLAlchemy & Alembic community
