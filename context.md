# Match Prediction App - Project Context

## Overview
This is a **Match Prediction Application** built as an MVP for predicting French Ligue 1 football match outcomes using machine learning.

## Architecture
The application follows a **micro-service architecture** with three main components:

```
┌─────────────────────────────────────────────────────────────┐
│                    Match Prediction App                         │
├──────────────────┬──────────────────┬────────────────────────┤
│   FastAPI_App     │    FastAPI_ML     │  match_prediction_app-  │
│  (Port: 8000)     │   (Port: 8001)     │        front            │
│                   │                    │                        │
│ - User Auth (JWT) │ - ML Model Mgmt    │ - Vue.js 3 Frontend     │
│ - User Profiles   │ - Match Data       │ - Consumes API (8000)   │
│ - Favorites       │ - Team Data        │ - JWT Auth Integration  │
│ - Prediction Hx   │ - Training Endpts  │                        │
│ - Proxy to ML API │ - Prediction Endpts │                        │
└──────────────────┴──────────────────┴────────────────────────┘
                          │                    │
                          ▼                    ▼
            ┌─────────────────────┐  ┌─────────────────────┐
            │  footballapp_db       │  │  footballml_db        │
            │  (PostgreSQL:5432)   │  │  (PostgreSQL:5432)   │
            │ - Users              │  │ - Teams              │
            │ - Predictions        │  │ - Matches            │
            │ - Favorites          │  │ - Statistics         │
            └─────────────────────┘  └─────────────────────┘
```

## Data Flow

```
Frontend (8080) 
  → POST /auth/login (8000) → Returns JWT Token
  → GET /predictions/teams (8000) → Proxied to ML API (8001)
  → POST /predictions (8000) → Stored in App DB + Calls ML API
  → GET /predictions/history (8000) → From App DB
```

## Technology Stack

| Component | Technology |
|-----------|------------|
| **Backend (App)** | FastAPI, Python 3.12+, SQLAlchemy, Pydantic |
| **Backend (ML)** | FastAPI, Python 3.12+, scikit-learn, pandas |
| **Frontend** | Vue.js 3, Vue Router, Axios |
| **Database** | PostgreSQL (2 separate databases) |
| **Auth** | JWT (HS256 algorithm) |
| **ML Model** | Classification model (scikit-learn) |
| **Tests** | pytest (backend), Jest (frontend) |

## Key Files & Directories

```
Match-Prediction-App/
├── .env                    # Shared configuration for both APIs
├── .env.example            # Template for environment variables
├── docker-compose.yml      # Docker orchestration
├── Makefile                # Useful commands
├── 
├── Data/                   # Database scripts & datasets
│   ├── MCD.sql             # ML database schema
│   ├── MCD_app.sql         # Application database schema
│   └── dataset/            # ML datasets & models
├── 
├── FastAPI_App/            # Application API (Port: 8000)
│   ├── app/
│   │   ├── main.py         # FastAPI app entry point
│   │   ├── routes/         # API endpoints
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── database.py     # SQLAlchemy config
│   └── requirements.txt
├── 
├── FastAPI_ML/              # ML API (Port: 8001)
│   ├── app/
│   │   ├── main.py         # FastAPI app entry point
│   │   ├── routes/         # ML endpoints (/train, /predict, /metrics)
│   │   ├── models/         # ML data models
│   │   ├── schemas/        # ML schemas
│   │   ├── services/       # ML services
│   │   └── database.py     # ML database config
│   └── requirements.txt
├── 
├── match_prediction_app-front/  # Vue.js Frontend (Port: 8080)
│   ├── src/
│   │   ├── api/client.js   # Axios client with JWT interceptor
│   │   ├── router/         # Vue Router with auth guards
│   │   └── ...
│   └── package.json
└── 
└── shared/                 # Shared code between APIs
    └── config/             # Shared configuration
```

## Environment Variables

All configuration is centralized in the **root `.env` file**:

```env
# Database URLs
DATABASE_APP_URL=postgresql://user:pass@localhost:5432/footballapp_db
DATABASE_ML_URL=postgresql://user:pass@localhost:5432/footballml_db
DATABASE_URL=postgresql://user:pass@localhost:5432/footballapp_db

# ML Service URL
ML_API_URL=http://localhost:8001

# JWT Configuration (App API)
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# ML Configuration
MODEL_PATH=../Data/dataset/match_model_v1.joblib
DATASET_PATH=../Data/dataset/completed_match_dataset_final.csv
DATA_DIR=../Data
```

## Running the Application

1. **Start databases** (if using Docker):
   ```bash
   docker-compose up -d
   ```

2. **Initialize databases**:
   ```bash
   psql -U postgres -f Data/MCD.sql
   psql -U postgres -f Data/MCD_app.sql
   ```

3. **Start APIs**:
   ```bash
   # App API (Port: 8000)
   cd FastAPI_App
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   
   # ML API (Port: 8001)
   cd FastAPI_ML
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
   ```

4. **Start Frontend**:
   ```bash
   cd match_prediction_app-front
   npm run serve
   ```

## API Endpoints

### App API (Port: 8000)
- `GET /health` - Health check
- `POST /auth/register` - User registration
- `POST /auth/login` - User login (returns JWT)
- `GET /auth/me` - Current user info
- `GET /predictions/teams` - List of teams (proxied from ML API)
- `POST /predictions` - Create a prediction
- `GET /predictions/history` - User's prediction history
- `POST /favorites` - Add to favorites
- `GET /favorites` - List favorites

### ML API (Port: 8001)
- `GET /health` - Health check
- `GET /teams` - List all teams
- `GET /matches` - List matches
- `POST /train` - Train the model
- `POST /predict` - Make a prediction
- `GET /metrics` - Model metrics

## Testing

- **Backend tests**:
  ```bash
  cd FastAPI_App
  pytest tests/
  
  cd FastAPI_ML
  pytest tests_ml/  # ML-specific tests
  pytest tests_integration/  # Integration tests
  ```

- **Frontend tests**:
  ```bash
  cd match_prediction_app-front
  npm run test
  ```

## Project Origins

This project was developed as part of a **5-week MVP sprint** for a startup simulation, with the following constraints:
- Must use a **classification model**
- Must integrate **2+ external data sources**
- Must have **separate databases** for App and ML
- Must include **automated tests**
- Must follow **Agile methodology** (Sprints, Epics, User Stories)

See `brief.md` for the original project brief and requirements.
