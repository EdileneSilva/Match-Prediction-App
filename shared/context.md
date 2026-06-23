# Shared - Common Utilities Context

## Purpose
This directory contains **shared code, configuration, and utilities** used by both the Application API (`FastAPI_App`) and the ML API (`FastAPI_ML`).

## Structure

```
shared/
├── __init__.py              # Package initialization
├── config/                 # Shared configuration modules
│   ├── __init__.py
│   ├── database.py          # Database connection utilities
│   ├── settings.py          # Common settings and constants
│   ├── logging.py           # Logging configuration
│   └── exceptions.py        # Custom exception classes
└── utils/                  # (Future) Shared utility functions
    ├── __init__.py
    ├── validators.py        # Shared validation functions
    ├── helpers.py           # General helper functions
    └── serializers.py       # Shared serialization utilities
```

## Config Module

### database.py
**Purpose**: Provides shared database connection utilities and configuration.

**Key Functions/Classes**:
- `get_database_url()`: Returns the appropriate database URL based on environment
- `create_sync_engine(url)`: Creates a SQLAlchemy sync engine
- `create_async_engine(url)`: Creates a SQLAlchemy async engine
- `get_session_maker(engine)`: Creates a session factory
- `Base`: Common declarative base for SQLAlchemy models

**Usage**:
```python
# In FastAPI_App or FastAPI_ML
from shared.config.database import get_database_url, create_sync_engine

database_url = get_database_url()
engine = create_sync_engine(database_url)
```

### settings.py
**Purpose**: Centralized configuration settings for both APIs.

**Key Settings**:
- Database connection strings
- API URLs (ML_API_URL, FRONTEND_URL)
- JWT configuration
- Logging configuration
- CORS settings
- Rate limiting settings
- Model paths and dataset paths

**Usage**:
```python
from shared.config.settings import settings

# Access settings
app_name = settings.APP_NAME
ml_api_url = settings.ML_API_URL
jwt_secret = settings.SECRET_KEY
```

**Settings Class**:
```python
# shared/config/settings.py
from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "Match Prediction App"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database URLs
    DATABASE_APP_URL: str = "postgresql://amaury@localhost:5432/footballapp_db"
    DATABASE_ML_URL: str = "postgresql://amaury@localhost:5432/footballml_db"
    
    # API URLs
    ML_API_URL: str = "http://localhost:8001"
    FRONTEND_URL: str = "http://localhost:8080"
    
    # JWT Configuration
    SECRET_KEY: str = "change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # ML Configuration
    MODEL_PATH: str = "../Data/dataset/match_model_v1.joblib"
    DATASET_PATH: str = "../Data/dataset/completed_match_dataset_final.csv"
    DATA_DIR: str = "../Data"
    
    # CORS
    CORS_ORIGINS: str = "*"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = "../.env"  # Read from root .env file

settings = Settings()
```

### logging.py
**Purpose**: Centralized logging configuration for consistent logging across both APIs.

**Key Components**:
- Logger configuration
- Log formatters
- Log handlers (console, file)
- Log levels

**Usage**:
```python
from shared.config.logging import get_logger

logger = get_logger(__name__)
logger.info("Application started")
logger.error("Error occurred", exc_info=True)
```

**Configuration**:
```python
# shared/config/logging.py
import logging
import sys
from typing import Optional

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

def configure_logging(log_level: str = "INFO") -> None:
    """Configure logging for the application."""
    logging.basicConfig(
        level=log_level,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("app.log"),
        ],
    )

def get_logger(name: str, log_level: Optional[str] = None) -> logging.Logger:
    """Get a configured logger with the given name."""
    logger = logging.getLogger(name)
    if log_level:
        logger.setLevel(log_level)
    return logger
```

### exceptions.py
**Purpose**: Custom exception classes used across both APIs for consistent error handling.

**Common Exceptions**:
- `AppException`: Base exception for the application
- `DatabaseException`: Database-related errors
- `ValidationException`: Data validation errors
- `AuthenticationException`: Authentication-related errors
- `AuthorizationException`: Authorization/permission errors
- `NotFoundException`: Resource not found errors
- `MLException`: Machine learning-specific errors

**Usage**:
```python
from shared.config.exceptions import NotFoundException, ValidationException

# Raise a not found exception
raise NotFoundException("User not found")

# Raise a validation exception
raise ValidationException("Invalid input data", errors=["Field X is required"])
```

**Exception Classes**:
```python
# shared/config/exceptions.py
class AppException(Exception):
    """Base exception for the application."""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class NotFoundException(AppException):
    """Resource not found exception."""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)

class ValidationException(AppException):
    """Data validation exception."""
    def __init__(self, message: str = "Validation error", errors: list = None):
        self.errors = errors or []
        super().__init__(message, status_code=400)

class AuthenticationException(AppException):
    """Authentication exception."""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401)

class AuthorizationException(AppException):
    """Authorization exception."""
    def __init__(self, message: str = "Permission denied"):
        super().__init__(message, status_code=403)

class DatabaseException(AppException):
    """Database exception."""
    def __init__(self, message: str = "Database error"):
        super().__init__(message, status_code=500)

class MLException(AppException):
    """Machine learning exception."""
    def __init__(self, message: str = "ML processing error"):
        super().__init__(message, status_code=500)
```

## Shared Utilities

### validators.py
**Purpose**: Shared validation functions used across both APIs.

**Common Validators**:
- `validate_email(email)`: Validate email format
- `validate_password(password)`: Validate password strength
- `validate_uuid(uuid_str)`: Validate UUID format
- `validate_date(date_str)`: Validate date format
- `validate_positive_int(value)`: Validate positive integer
- `validate_range(value, min_val, max_val)`: Validate value in range

### helpers.py
**Purpose**: General utility functions.

**Common Helpers**:
- `camel_to_snake(name)`: Convert CamelCase to snake_case
- `snake_to_camel(name)`: Convert snake_case to CamelCase
- `generate_uuid()`: Generate a UUID
- `get_current_timestamp()`: Get current timestamp
- `deep_merge(dict1, dict2)`: Deep merge dictionaries
- `flatten_dict(d, parent_key='')`: Flatten nested dictionary

### serializers.py
**Purpose**: Shared serialization utilities for consistent JSON responses.

**Common Serializers**:
- `serialize_model(model)`: Convert SQLAlchemy model to dict
- `serialize_list(models)`: Convert list of models to list of dicts
- `serialize_datetime(dt)`: Convert datetime to ISO format string
- `serialize_decimal(d)`: Convert Decimal to float
- `serialize_uuid(uuid)`: Convert UUID to string

## Usage Pattern

Both `FastAPI_App` and `FastAPI_ML` import from the shared module:

```python
# In FastAPI_App/app/main.py
from shared.config.settings import settings
from shared.config.logging import get_logger
from shared.config.exceptions import NotFoundException

logger = get_logger(__name__)

@app.get("/health")
def health_check():
    logger.info("Health check endpoint called")
    return {"status": "ok", "service": settings.APP_NAME}
```

```python
# In FastAPI_ML/app/main.py
from shared.config.settings import settings
from shared.config.database import get_database_url

DATABASE_URL = get_database_url()
# Use DATABASE_URL for SQLAlchemy
```

## Python Path Configuration

For the shared module to be importable from both APIs, ensure the root directory is in the Python path:

```python
# Both FastAPI_App and FastAPI_ML should have their PYTHONPATH set
# Option 1: Set in the shell before running
# export PYTHONPATH=/path/to/Match-Prediction-App:$PYTHONPATH

# Option 2: Use a .env file
PYTHONPATH=/home/edilene/Dropbox/Simplon_Projects/Match-Prediction-App

# Option 3: Add to sys.path in your code
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
```

## Development Guidelines

### Adding Shared Code

1. **Identify common functionality** that is needed in both APIs
2. **Create a new module** in the appropriate subdirectory
3. **Import and use** the shared code in both APIs
4. **Document** the new functionality in this context.md

### Example: Adding a Shared Utility

```python
# shared/utils/date_utils.py
from datetime import datetime, timedelta
from typing import Optional

def parse_date(date_str: str, fmt: str = "%Y-%m-%d") -> datetime:
    """Parse a date string into a datetime object."""
    return datetime.strptime(date_str, fmt)

def format_date(dt: datetime, fmt: str = "%Y-%m-%d") -> str:
    """Format a datetime object into a string."""
    return dt.strftime(fmt)

def get_days_between(dt1: datetime, dt2: datetime) -> int:
    """Get the number of days between two dates."""
    return abs((dt1 - dt2).days)
```

Then use it in both APIs:
```python
from shared.utils.date_utils import parse_date, format_date

date_obj = parse_date("2024-01-01")
formatted = format_date(date_obj)
```

## Best Practices

1. **Keep shared code minimal**: Only put code here that is genuinely used by both APIs
2. **Document thoroughly**: Shared code should have clear documentation
3. **Test shared code**: Add tests for shared utilities in both API test suites
4. **Version compatibility**: Ensure shared code is compatible with all using APIs
5. **Avoid circular dependencies**: Shared code should not depend on API-specific code

## Future Enhancements

Potential additions to the shared module:
- **Common database models**: Base models that both APIs extend
- **API client**: Shared client for inter-service communication
- **Authentication utilities**: Common JWT handling functions
- **Validation schemas**: Shared Pydantic schemas
- **Testing utilities**: Common test fixtures and helpers
- **Metrics tracking**: Shared metrics and monitoring utilities
- **Cache utilities**: Shared caching mechanisms

## Testing Shared Code

Since shared code is used by both APIs, it should be tested in both contexts:

```python
# In FastAPI_App/tests/test_shared.py
def test_shared_validators():
    from shared.utils.validators import validate_email
    assert validate_email("test@example.com") == True
    assert validate_email("invalid") == False

# In FastAPI_ML/tests_ml/test_shared.py
def test_shared_helpers():
    from shared.utils.helpers import camel_to_snake
    assert camel_to_snake("CamelCase") == "camel_case"
```

Alternatively, create a separate `tests/` directory in the shared module:

```
shared/
├── config/
├── utils/
└── tests/
    ├── test_validators.py
    └── test_helpers.py
```
