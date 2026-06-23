# FastAPI_App - Application API Context

## Purpose
This is the **Application API** component of the Match Prediction App, running on **port 8000**.

## Responsibilities

This API handles:
- **Authentication**: JWT-based user authentication (register, login, me)
- **User Management**: User profiles, favorites
- **Prediction History**: User's past predictions and results
- **Proxy Layer**: Routes requests to the ML API when needed
- **Business Logic**: Application-level logic and data validation

## Architecture

```
FastAPI_App/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # SQLAlchemy database connection
│   ├── 
│   ├── core/               # Core utilities and config
│   │   └── config.py        # Application configuration
│   │
│   ├── models/             # SQLAlchemy ORM models
│   │   ├── user.py          # User model
│   │   ├── prediction.py    # Prediction model
│   │   └── favorite.py      # Favorite model
│   │
│   ├── schemas/            # Pydantic request/response schemas
│   │   ├── user.py          # User schemas
│   │   ├── prediction.py    # Prediction schemas
│   │   ├── favorite.py      # Favorite schemas
│   │   └── auth.py          # Auth schemas (Token, TokenData)
│   │
│   ├── routes/             # FastAPI route handlers
│   │   ├── auth.py          # /auth/* endpoints
│   │   ├── users.py         # /users/* endpoints
│   │   ├── predictions.py   # /predictions/* endpoints
│   │   └── favorites.py     # /favorites/* endpoints
│   │
│   ├── services/           # Business logic services
│   │   ├── auth.py          # Auth service
│   │   ├── user.py          # User service
│   │   ├── prediction.py    # Prediction service
│   │   └── favorite.py      # Favorite service
│   │
│   └── utils/              # Utility functions
│       ├── security.py      # JWT token handling
│       ├── dependencies.py  # FastAPI dependencies
│       └── helpers.py       # Helper functions
│
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container configuration
└── tests/                 # Unit and integration tests
    ├── conftest.py         # Pytest fixtures
    ├── test_auth.py        # Auth tests
    ├── test_users.py       # User tests
    └── test_predictions.py # Prediction tests
```

## Environment Variables

This API reads from the **root `.env` file**. Required variables:

```env
# Database Connection
DATABASE_APP_URL=postgresql://user:pass@localhost:5432/footballapp_db

# ML API URL (for proxying requests)
ML_API_URL=http://localhost:8001

# JWT Configuration
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## Key Dependencies

- **FastAPI**: Web framework
- **SQLAlchemy**: ORM for PostgreSQL
- **Pydantic**: Data validation
- **python-jose**: JWT encoding/decoding
- **passlib**: Password hashing
- **httpx**: HTTP client for proxying to ML API
- **python-dotenv**: Environment variable loading

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
  - Request: `{email: string, password: string, username: string}`
  - Response: `{user: User, access_token: string, token_type: string}`

- `POST /auth/login` - Login user
  - Request: `{email: string, password: string}`
  - Response: `{access_token: string, token_type: string, user: User}`

- `GET /auth/me` - Get current user (requires JWT)
  - Response: `{user: User}`

### Users
- `GET /users/{user_id}` - Get user by ID
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

### Predictions
- `GET /predictions/teams` - Get list of teams (proxied from ML API)
  - Response: `{teams: Team[]}`

- `POST /predictions` - Create a prediction
  - Request: `{match_id: int, home_team_score: int, away_team_score: int}`
  - Response: `{prediction: Prediction}`

- `GET /predictions/history` - Get user's prediction history
  - Response: `{predictions: Prediction[]}`

- `GET /predictions/{prediction_id}` - Get specific prediction

### Favorites
- `POST /favorites` - Add team to favorites
  - Request: `{team_id: int}`
  - Response: `{favorite: Favorite}`

- `GET /favorites` - Get user's favorite teams
  - Response: `{favorites: Favorite[]}`

- `DELETE /favorites/{favorite_id}` - Remove from favorites

### Health
- `GET /health` - Health check
  - Response: `{status: string, service: string}`

## Database Schema

The Application API uses the **footballapp_db** PostgreSQL database with these main tables:

- **users**: User accounts (id, email, username, hashed_password, created_at)
- **predictions**: User predictions (id, user_id, match_id, home_score, away_score, created_at)
- **favorites**: User's favorite teams (id, user_id, team_id, created_at)

See `../Data/MCD_app.sql` for the complete schema.

## Testing

Run tests with:
```bash
cd FastAPI_App
pytest tests/ -v
```

Test coverage includes:
- Authentication flow (register, login, token validation)
- User CRUD operations
- Prediction creation and retrieval
- Favorite management
- JWT token security
- Database interaction

## Development Workflow

1. **Install dependencies**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Run the API**:
   ```bash
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

3. **Test**:
   ```bash
   pytest tests/ -v
   ```

4. **Verify**:
   ```bash
   curl http://127.0.0.1:8000/health
   # Expected: {"status":"ok","service":"app-api"}
   ```

## Inter-service Communication

This API communicates with the ML API (`FastAPI_ML`) for:
- Fetching team data (`GET /predictions/teams` → `GET {ML_API_URL}/teams`)
- Making match predictions (internal calls to ML API)

The ML API URL is configurable via `ML_API_URL` environment variable.

## Security Considerations

- All sensitive endpoints require JWT authentication
- Passwords are hashed using bcrypt
- JWT tokens use HS256 algorithm
- Tokens expire after 60 minutes (configurable)
- CORS is configured to allow frontend domain

## Error Handling

Standard error responses follow this pattern:
```json
{
  "detail": "Error message",
  "status_code": 400
}
```

Common HTTP status codes:
- `400 Bad Request`: Validation errors
- `401 Unauthorized`: Missing or invalid JWT
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server errors
