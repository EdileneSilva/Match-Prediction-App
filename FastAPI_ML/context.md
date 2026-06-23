# FastAPI_ML - Machine Learning API Context

## Purpose
This is the **Machine Learning API** component of the Match Prediction App, running on **port 8001**.

## Responsibilities

This API handles:
- **Data Management**: Teams, matches, and match statistics
- **ML Model**: Training, prediction, and evaluation of the classification model
- **Match Data**: Historical match data and current season data
- **Metrics**: Model performance metrics and evaluation results

## Architecture

```
FastAPI_ML/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # SQLAlchemy database connection
│   ├── 
│   ├── core/               # Core utilities and config
│   │   └── config.py        # ML configuration
│   │
│   ├── models/             # SQLAlchemy ORM models
│   │   ├── team.py          # Team model
│   │   ├── match.py         # Match model
│   │   └── statistics.py    # Match statistics model
│   │
│   ├── schemas/            # Pydantic request/response schemas
│   │   ├── team.py          # Team schemas
│   │   ├── match.py         # Match schemas
│   │   ├── prediction.py    # Prediction input/output schemas
│   │   └── metrics.py       # Metrics schemas
│   │
│   ├── routes/             # FastAPI route handlers
│   │   ├── teams.py         # /teams/* endpoints
│   │   ├── matches.py       # /matches/* endpoints
│   │   ├── train.py         # /train endpoint
│   │   ├── predict.py       # /predict endpoint
│   │   └── metrics.py       # /metrics endpoint
│   │
│   ├── services/           # ML and data services
│   │   ├── team.py          # Team service
│   │   ├── match.py         # Match service
│   │   ├── model.py         # ML model service (training, prediction)
│   │   └── data_loader.py   # Data loading and preprocessing
│   │
│   └── utils/              # Utility functions
│       ├── preprocessor.py  # Data preprocessing
│       ├── features.py      # Feature engineering
│       └── metrics.py       # Metrics calculation
│
├── mlflow.db               # MLflow tracking database (optional)
├── mlruns/                 # MLflow experiment runs
├── pytest.ini              # Pytest configuration
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container configuration
├── tests_ml/               # ML-specific unit tests
│   ├── conftest.py
│   ├── test_models.py
│   ├── test_preprocessing.py
│   └── test_training.py
└── tests_integration/      # Integration tests
    ├── conftest.py
    ├── test_ml_api.py
    └── test_app_ml_integration.py
```

## Environment Variables

This API reads from the **root `.env` file**. Required variables:

```env
# Database Connection
DATABASE_ML_URL=postgresql://user:pass@localhost:5432/footballml_db

# ML Configuration
MODEL_PATH=../Data/dataset/match_model_v1.joblib
DATASET_PATH=../Data/dataset/completed_match_dataset_final.csv
DATA_DIR=../Data
```

## Key Dependencies

- **FastAPI**: Web framework
- **SQLAlchemy**: ORM for PostgreSQL
- **Pydantic**: Data validation
- **scikit-learn**: ML library (classification models)
- **pandas**: Data manipulation
- **numpy**: Numerical operations
- **joblib**: Model serialization
- **python-dotenv**: Environment variable loading
- **mlflow**: Experiment tracking (optional)

## API Endpoints

### Teams
- `GET /teams` - List all teams
  - Response: `{teams: Team[]}`

- `GET /teams/{team_id}` - Get specific team
  - Response: `{team: Team}`

- `POST /teams` - Create a team (admin)
- `PUT /teams/{team_id}` - Update a team (admin)
- `DELETE /teams/{team_id}` - Delete a team (admin)

### Matches
- `GET /matches` - List all matches
  - Query params: `team_id`, `date_from`, `date_to`, `limit`, `offset`
  - Response: `{matches: Match[], total: int}`

- `GET /matches/{match_id}` - Get specific match
  - Response: `{match: Match}`

- `POST /matches` - Create a match (admin)
- `PUT /matches/{match_id}` - Update a match (admin)

### Model Training
- `POST /train` - Train the ML model
  - Request: `{dataset_path?: string, model_params?: object}`
  - Response: `{status: string, model_path: string, metrics: Metrics}`

- `GET /train/status` - Get current training status
  - Response: `{status: string, progress: float, started_at: string}`

### Prediction
- `POST /predict` - Make a match prediction
  - Request: `{home_team_id: int, away_team_id: int, features?: object}`
  - Response: `{prediction: string, probabilities: object, match_id: int}`

### Metrics
- `GET /metrics` - Get model metrics
  - Response: `{accuracy: float, precision: float, recall: float, f1_score: float, confusion_matrix: array}`

- `GET /metrics/history` - Get historical metrics
  - Response: `{metrics: MetricsHistory[]}`

### Health
- `GET /health` - Health check
  - Response: `{status: string, service: string}`

## Database Schema

The ML API uses the **footballml_db** PostgreSQL database with these main tables:

- **teams**: Football teams (id, name, code, league, founded_year)
- **matches**: Match data (id, home_team_id, away_team_id, date, home_score, away_score, league, season)
- **statistics**: Match statistics (id, match_id, possession, shots, shots_on_target, etc.)

See `../Data/MCD.sql` for the complete schema.

## ML Pipeline

### Data Sources
1. **Internal Database**: Historical match data from footballml_db
2. **External APIs**: Football data APIs (e.g., Football-Data.org, API-FOOTBALL)
3. **CSV Files**: Pre-collected datasets in `Data/dataset/`

### Model Training
1. **Data Loading**: Load from database and CSV files
2. **Preprocessing**: Clean, normalize, handle missing values
3. **Feature Engineering**: Create features for the classification model
4. **Train/Test Split**: Split data (typically 80/20)
5. **Model Training**: Train classification model (e.g., RandomForest, XGBoost, Logistic Regression)
6. **Evaluation**: Calculate metrics (accuracy, precision, recall, F1)
7. **Serialization**: Save model to disk (joblib format)

### Prediction
1. **Input Validation**: Validate prediction request
2. **Feature Extraction**: Extract features from input data
3. **Model Loading**: Load trained model from disk
4. **Prediction**: Generate prediction and probabilities
5. **Response**: Return prediction result

## Model Configuration

The classification model uses the following approach:

**Target Variable**: Match outcome (Win/Lose/Draw for home team)

**Features** (typical):
- Team strength indicators (ELO rating, form)
- Head-to-head history
- Home/away performance
- Goals scored/conceded
- Possession statistics
- Shots and shots on target
- League position

**Model Options**:
- RandomForestClassifier (default)
- GradientBoostingClassifier
- XGBClassifier
- LogisticRegression
- SVM

## Testing

Run tests with:
```bash
cd FastAPI_ML

# ML-specific tests
pytest tests_ml/ -v

# Integration tests
pytest tests_integration/ -v

# All tests
pytest -v
```

Test coverage includes:
- Model training pipeline
- Data preprocessing and feature engineering
- Prediction accuracy
- API endpoint responses
- Database interactions
- Integration with App API

## Development Workflow

1. **Install dependencies**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Run the API**:
   ```bash
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
   ```

3. **Test**:
   ```bash
   pytest tests_ml/ tests_integration/ -v
   ```

4. **Verify**:
   ```bash
   curl http://127.0.0.1:8001/health
   # Expected: {"status":"ok","service":"ml-api"}
   ```

## Data Files

Key data files in `../Data/dataset/`:
- `completed_match_dataset_final.csv` - Main training dataset
- `match_model_v1.joblib` - Trained model file
- `team_data.csv` - Team information
- `fixtures.csv` - Upcoming matches

## Inter-service Communication

This API is consumed by:
- **FastAPI_App**: Proxies team data to frontend
- **Frontend**: Direct calls for match data and predictions (via App API proxy)

The App API communicates with this service via `ML_API_URL` environment variable.

## Model Evaluation Metrics

Primary metrics tracked:
- **Accuracy**: Overall prediction accuracy
- **Precision**: Precision for each class (Win/Lose/Draw)
- **Recall**: Recall for each class
- **F1 Score**: Harmonic mean of precision and recall
- **Confusion Matrix**: Full classification performance breakdown
- **ROC AUC**: Area under ROC curve (for probabilistic predictions)

Target performance:
- Accuracy: >70%
- F1 Score (balanced): >0.7
- Precision/Recall: >0.7 for each class
