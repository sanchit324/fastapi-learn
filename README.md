# FastAPI Social Media API

A robust, production-ready RESTful API built with FastAPI, SQLAlchemy, and PostgreSQL, featuring user authentication, post management, and voting system.

## ✨ Features

- **User Authentication**
  - JWT-based authentication
  - Secure password hashing with bcrypt
  - Token-based authorization

- **Posts Management**
  - Create, read, update, and delete posts
  - Pagination and search functionality
  - User-specific post ownership

- **Voting System**
  - Upvote/downvote posts
  - Prevent duplicate votes
  - Track post popularity

- **Database**
  - PostgreSQL database
  - SQLAlchemy ORM
  - Alembic for database migrations

## 🚀 Prerequisites

- Python 3.8+
- PostgreSQL
- pip (Python package manager)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd fastapi
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🔧 Environment Setup

1. Create a `.env` file in the root directory:
   ```env
   # Database
   DATABASE_HOSTNAME=localhost
   DATABASE_PORT=5432
   DATABASE_NAME=fastapi
   DATABASE_USERNAME=your_username
   DATABASE_PASSWORD=your_password

   # JWT Authentication
   SECRET_KEY=your_secret_key_here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

## 🗄️ Database Setup

1. **Create a PostgreSQL database**
   ```sql
   CREATE DATABASE fastapi;
   ```

2. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

## 🏃 Running the Application

1. **Start the development server**
   ```bash
   uvicorn app.main:app --reload
   ```
   - `app.main:app` tells uvicorn to look for the FastAPI app in `app/main.py`
   - `--reload` enables auto-reload for development (remove in production)

2. **Access the API documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 📚 API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - Register new user

### Users
- `GET /users/` - Get current user
- `GET /users/{id}` - Get user by ID
- `POST /users/` - Create new user

### Posts
- `GET /posts/` - Get all posts
- `GET /posts/{id}` - Get post by ID
- `POST /posts/` - Create new post
- `PUT /posts/{id}` - Update post
- `DELETE /posts/{id}` - Delete post

### Votes
- `POST /votes/` - Vote on a post

## 🔐 Authentication

1. Register a new user at `POST /auth/register`
2. Login at `POST /auth/login` to get a JWT token
3. Include the token in the `Authorization` header for protected routes:
   ```
   Authorization: Bearer <your_token>
   ```
   
## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Built with ❤️ using FastAPI
