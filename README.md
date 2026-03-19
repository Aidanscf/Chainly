# Professional FastAPI Project Structure

## Project Overview
Complete FastAPI application with professional folder structure and user authentication system including:
- User registration and login
- JWT token-based authentication
- Password hashing and security
- User profile management
- Role-based access control (RBAC)
- SQLAlchemy ORM integration
- Pydantic data validation
- CORS middleware
- Comprehensive error handling

## Folder Structure

```
Chainly_backend/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py          # Authentication endpoints
│   │   │   │   └── users.py         # User management endpoints
│   │   │   └── __init__.py
│   │   ├── __init__.py              # API router configuration
│   │   └── dependencies.py          # Dependency injection (JWT auth)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                # Application configuration
│   │   └── security.py              # Security utilities (JWT, password hashing)
│   ├── db/
│   │   ├── __init__.py
│   │   └── database.py              # Database connection and session
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py                  # User SQLAlchemy model
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py                  # Pydantic schemas for validation
│   ├── services/
│   │   ├── __init__.py
│   │   └── user.py                  # User business logic
│   ├── middleware/
│   │   └── __init__.py              # Custom middleware
│   ├── main.py                      # FastAPI application factory
│   └── __init__.py
├── main.py                          # Entry point
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
└── README.md                        # This file

```

## Installation

### 1. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 4. Run the application
```bash
python main.py
```

Application will be available at: `http://localhost:8000`

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Authentication Endpoints

### Register
```
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "securepassword",
  "full_name": "User Name"
}
```

### Login
```
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}

Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### Refresh Token
```
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Get Current User
```
GET /api/v1/auth/me
Authorization: Bearer <access_token>
```

### Change Password
```
POST /api/v1/auth/change-password
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "old_password": "oldpassword",
  "new_password": "newpassword"
}
```

## User Management Endpoints

### List All Users (Admin Only)
```
GET /api/v1/users/?skip=0&limit=10
Authorization: Bearer <access_token>
```

### Get User Profile
```
GET /api/v1/users/{user_id}
Authorization: Bearer <access_token>
```

### Update User Profile
```
PUT /api/v1/users/{user_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "email": "newemail@example.com",
  "username": "newusername",
  "full_name": "New Name"
}
```

### Delete User (Deactivate)
```
DELETE /api/v1/users/{user_id}
Authorization: Bearer <access_token>
```

## Security Features

### Password Hashing
- Uses bcrypt for secure password hashing
- Passwords never stored in plain text
- Configurable hash rounds

### JWT Tokens
- Access tokens for short-lived authentication
- Refresh tokens for obtaining new access tokens
- Configurable expiration times
- Token validation on protected routes

### CORS Configuration
- Configurable allowed origins
- Supports multiple domains
- Environment-based configuration

### Input Validation
- Pydantic models for automatic validation
- Email validation
- Password strength requirements
- Username uniqueness checks

### Access Control
- Role-based access control (superuser/regular user)
- User can only modify own profile
- Superusers can manage all users
- Protected endpoints with dependency injection

## Configuration

Edit `app/core/config.py` or `.env` file:

```
PROJECT_NAME=Chainly API
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

## Database

### Migrations with Alembic (Optional)

```bash
# Initialize alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

## Testing

```bash
pytest
pytest -v  # Verbose output
pytest --cov=app  # With coverage
```

## Development Best Practices

1. **Environment Variables**: Always use `.env` for sensitive data
2. **Database**: Currently uses SQLite. For production, use PostgreSQL
3. **Secret Key**: Generate a strong secret key for production
4. **CORS**: Configure allowed origins properly for security
5. **Error Handling**: All endpoints have proper error handling
6. **Logging**: Implement logging in services
7. **Rate Limiting**: Consider adding rate limiting for production
8. **Validation**: Always validate user input

## Common Issues

### Import Errors
Ensure all dependencies are installed: `pip install -r requirements.txt`

### Database Lock (SQLite)
If using SQLite in production, consider PostgreSQL

### CORS Issues
Update `CORS_ORIGINS` in `.env` to include your frontend domain

## Production Deployment

1. Use PostgreSQL instead of SQLite
2. Generate strong SECRET_KEY
3. Set `reload=False` in production
4. Use environment variables for all sensitive data
5. Enable HTTPS
6. Implement rate limiting
7. Add request logging
8. Set up monitoring and alerting

## License

MIT

## Support

For issues and feature requests, contact: support@example.com
