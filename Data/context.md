# Data - Database & Dataset Context

## Purpose
This directory contains all **database schemas, SQL scripts, datasets, and ML model files** for the Match Prediction App.

## Structure

```
Data/
├── MCD.sql                 # ML Database schema (footballml_db)
├── MCD_app.sql             # Application Database schema (footballapp_db)
├── docker-entrypoint-initdb.d/  # Docker database initialization scripts
│   └── init.sql            # Initial data seeding
├── dataset/                # ML datasets and models
│   ├── completed_match_dataset_final.csv  # Main training dataset
│   ├── match_model_v1.joblib               # Trained ML model
│   ├── team_data.csv                      # Team information
│   ├── fixtures.csv                       # Upcoming matches
│   ├── historical_matches.csv            # Historical match data
│   ├── player_stats.csv                   # Player statistics
│   └── processed/                         # Processed datasets
│       ├── features.csv
│       └── labels.csv
├── MCD.png                 # Entity-Relationship Diagram (ML database)
└── MCD.sql                 # Backup copy of ML schema
```

## Databases

The application uses **two separate PostgreSQL databases**:

### 1. footballml_db (ML Database)
**Purpose**: Stores match data, team information, and statistics for ML training and prediction.

**Schema**: Defined in `Data/MCD.sql`

**Tables**:

#### Teams
```sql
CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(10) NOT NULL UNIQUE,
    league VARCHAR(50) NOT NULL DEFAULT 'Ligue 1',
    founded_year INTEGER,
    stadium VARCHAR(100),
    city VARCHAR(100),
    logo_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Matches
```sql
CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    home_team_id INTEGER REFERENCES teams(id) ON DELETE CASCADE,
    away_team_id INTEGER REFERENCES teams(id) ON DELETE CASCADE,
    date TIMESTAMP NOT NULL,
    home_score INTEGER,
    away_score INTEGER,
    league VARCHAR(50) NOT NULL DEFAULT 'Ligue 1',
    season VARCHAR(50) NOT NULL,
    matchday INTEGER,
    status VARCHAR(20) NOT NULL DEFAULT 'FINISHED', -- FINISHED, POSTPONED, CANCELLED
    venue VARCHAR(100),
    referee VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Statistics
```sql
CREATE TABLE statistics (
    id SERIAL PRIMARY KEY,
    match_id INTEGER REFERENCES matches(id) ON DELETE CASCADE,
    team_id INTEGER REFERENCES teams(id) ON DELETE CASCADE,
    is_home BOOLEAN NOT NULL,
    possession DECIMAL(5,2), -- Percentage
    total_shots INTEGER,
    shots_on_target INTEGER,
    shots_off_target INTEGER,
    blocked_shots INTEGER,
    corners INTEGER,
    offsides INTEGER,
    fouls INTEGER,
    yellow_cards INTEGER,
    red_cards INTEGER,
    saves INTEGER,
    passes INTEGER,
    accurate_passes INTEGER,
    tackles INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. footballapp_db (Application Database)
**Purpose**: Stores user data, predictions, favorites, and application state.

**Schema**: Defined in `Data/MCD_app.sql`

**Tables**:

#### Users
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(100) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN NOT NULL DEFAULT true,
    is_superuser BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Predictions
```sql
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    match_id INTEGER,
    home_team_id INTEGER REFERENCES teams(id) ON DELETE SET NULL,
    away_team_id INTEGER REFERENCES teams(id) ON DELETE SET NULL,
    home_team_score INTEGER NOT NULL,
    away_team_score INTEGER NOT NULL,
    predicted_outcome VARCHAR(20), -- WIN, LOSE, DRAW
    confidence DECIMAL(5,2), -- Confidence percentage
    points INTEGER DEFAULT 0, -- Points earned (if correct)
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING', -- PENDING, CORRECT, INCORRECT
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Favorites
```sql
CREATE TABLE favorites (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    team_id INTEGER REFERENCES teams(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, team_id)
);
```

## Dataset Files

### completed_match_dataset_final.csv
**Purpose**: Main training dataset for the ML model

**Columns**:
- `match_id`: Unique match identifier
- `date`: Match date
- `season`: Season (e.g., "2022-2023")
- `league`: League name (e.g., "Ligue 1")
- `home_team`: Home team name
- `away_team`: Away team name
- `home_score`: Home team goals
- `away_score`: Away team goals
- `result`: Match outcome (WIN, LOSE, DRAW from home perspective)
- `home_possession`: Home team possession %
- `away_possession`: Away team possession %
- `home_shots`: Home team total shots
- `away_shots`: Away team total shots
- `home_shots_on_target`: Home team shots on target
- `away_shots_on_target`: Away team shots on target
- `home_corners`: Home team corners
- `away_corners`: Away team corners
- `home_fouls`: Home team fouls
- `away_fouls`: Away team fouls
- `home_yellow_cards`: Home team yellow cards
- `away_yellow_cards`: Away team yellow cards
- `home_red_cards`: Home team red cards
- `away_red_cards`: Away team red cards
- `home_team_elo`: Home team ELO rating before match
- `away_team_elo`: Away team ELO rating before match
- `home_team_form`: Home team form (points from last 5 matches)
- `away_team_form`: Away team form (points from last 5 matches)
- `head_to_head_home_wins`: Historical home wins vs this opponent
- `head_to_head_away_wins`: Historical away wins vs this opponent
- `head_to_head_draws`: Historical draws vs this opponent

**Target Variable**: `result` (WIN, LOSE, DRAW)

### team_data.csv
**Purpose**: Team metadata and information

**Columns**:
- `team_id`: Team identifier
- `name`: Team name
- `code`: Team code (e.g., "PSG", "OL", "OM")
- `league`: League
- `founded_year`: Year founded
- `stadium`: Stadium name
- `city`: City
- `capacity`: Stadium capacity
- `manager`: Current manager

### fixtures.csv
**Purpose**: Upcoming matches for prediction

**Columns**:
- `match_id`: Match identifier
- `date`: Match date
- `home_team`: Home team name
- `away_team`: Away team name
- `league`: League
- `season`: Season
- `matchday`: Matchday number

## ML Model Files

### match_model_v1.joblib
**Purpose**: Trained classification model for match prediction

**Model Type**: RandomForestClassifier (or other scikit-learn classifier)

**Features Used**:
1. Team ELO ratings (home and away)
2. Team form (points from last 5 matches)
3. Head-to-head statistics
4. Home/away performance indicators
5. Possession statistics (average)
6. Shot statistics (average)
7. Discipline statistics (average cards)
8. League position (if available)

**Target**: Match outcome (WIN, LOSE, DRAW)

**Training Process**:
1. Load data from `completed_match_dataset_final.csv`
2. Preprocess: Handle missing values, encode categorical variables
3. Feature engineering: Create derived features
4. Train/test split: 80% train, 20% test
5. Model training: RandomForestClassifier with 100 trees
6. Evaluation: Calculate accuracy, precision, recall, F1 score
7. Save model: Serialized to joblib format

## Docker Database Setup

The `docker-entrypoint-initdb.d/` directory contains scripts that run when the PostgreSQL containers start for the first time.

### docker-compose.yml Configuration

```yaml
services:
  postgres-app:
    image: postgres:15
    environment:
      POSTGRES_DB: footballapp_db
      POSTGRES_USER: amaury
      POSTGRES_PASSWORD: password
    volumes:
      - ./Data/docker-entrypoint-initdb.d:/docker-entrypoint-initdb.d
    ports:
      - "5432:5432"

  postgres-ml:
    image: postgres:15
    environment:
      POSTGRES_DB: footballml_db
      POSTGRES_USER: amaury
      POSTGRES_PASSWORD: password
    volumes:
      - ./Data/docker-entrypoint-initdb.d:/docker-entrypoint-initdb.d
    ports:
      - "5433:5432"
```

### Initialization Script (docker-entrypoint-initdb.d/init.sql)

```sql
-- Create schemas if they don't exist
-- Insert initial data (teams, sample matches, etc.)
-- This runs only on first container startup
```

## Data Sources

The project integrates **multiple external data sources** as required:

### 1. API Data Sources
- **Football-Data.org API**: Official football data API
  - Endpoints: `/competitions`, `/teams`, `/matches`
  - Data: Live match data, team information, competition structure
- **API-FOOTBALL**: Alternative football API
  - Data: Historical match data, statistics, standings

### 2. CSV File Sources
- **FBref (Sports Reference)**: Scraped CSV files
  - Match statistics
  - Player data
  - Team performance metrics
- **Open Football**: Historical datasets
  - Historical match results (1990s - present)
  - League structures
  - Team information

### 3. Web Scraping Sources
- **LFP (Ligue de Football Professionnel)**: Official Ligue 1 website
- **L'Equipe**: French sports news and statistics
- **Foot Mercato**: Transfer and team news

## Data Collection Scripts

While not currently in the repository, the following scripts were used for data collection:

```python
# Example: Collect data from Football-Data.org API
import requests
import pandas as pd

API_KEY = "your_api_key"
BASE_URL = "https://api.football-data.org/v4"

# Get Ligue 1 teams
response = requests.get(
    f"{BASE_URL}/competitions/FL1/teams",
    headers={"X-Auth-Token": API_KEY}
)
teams_data = response.json()

# Get matches for current season
response = requests.get(
    f"{BASE_URL}/competitions/FL1/matches",
    headers={"X-Auth-Token": API_KEY},
    params={"season": "2023"}
)
matches_data = response.json()
```

## Data Preprocessing

The data preprocessing pipeline includes:

1. **Data Cleaning**:
   - Handle missing values (imputation or removal)
   - Remove duplicates
   - Fix data type inconsistencies
   - Handle outliers

2. **Feature Engineering**:
   - Calculate team form (points from last N matches)
   - Compute ELO ratings
   - Aggregate head-to-head statistics
   - Calculate rolling averages
   - Create interaction features

3. **Data Transformation**:
   - Encode categorical variables (team names, leagues)
   - Normalize numerical features
   - Scale features (StandardScaler)
   - Create target variable (result encoding)

4. **Train/Test Split**:
   - Stratified split to maintain class distribution
   - Time-based split for temporal data
   - Cross-validation for model evaluation

## Data Quality Metrics

### Dataset Statistics (completed_match_dataset_final.csv)
- **Total Matches**: ~10,000+ Ligue 1 matches
- **Seasons Covered**: 2000-2001 to 2022-2023
- **Teams**: 20 Ligue 1 teams per season
- **Features**: 25+ features per match
- **Target Classes**:
  - WIN: ~45%
  - LOSE: ~45%
  - DRAW: ~10%

### Data Quality Checks
- **Completeness**: >95% of key features populated
- **Consistency**: All match outcomes validated
- **Accuracy**: Data cross-validated with multiple sources
- **Recency**: Data includes most recent completed season

## Backup and Versioning

### Database Backups
```bash
# Create backup
pg_dump -U username -d footballml_db -F c -f backup_footballml_$(date +%Y%m%d).dump
pg_dump -U username -d footballapp_db -F c -f backup_footballapp_$(date +%Y%m%d).dump

# Restore backup
pg_restore -U username -d footballml_db backup_footballml_20240101.dump
```

### Dataset Versioning
All datasets and models are versioned:
- `match_model_v1.joblib` - Version 1 of the model
- `completed_match_dataset_v1.csv` - Version 1 of the dataset
- Future versions follow semantic versioning

## Common Data Operations

### Importing Data to PostgreSQL

```bash
# Import teams
psql -U username -d footballml_db -c "\COPY teams FROM '/path/to/team_data.csv' DELIMITER ',' CSV HEADER"

# Import matches
psql -U username -d footballml_db -c "\COPY matches FROM '/path/to/completed_match_dataset_final.csv' DELIMITER ',' CSV HEADER"
```

### Exporting Data from PostgreSQL

```bash
# Export teams
psql -U username -d footballml_db -c "\COPY (SELECT * FROM teams) TO '/path/to/teams_export.csv' DELIMITER ',' CSV HEADER"

# Export recent matches
psql -U username -d footballml_db -c "\COPY (SELECT * FROM matches WHERE season = '2022-2023') TO '/path/to/matches_2023.csv' DELIMITER ',' CSV HEADER"
```

## Performance Optimization

### Indexes
The following indexes should be created for optimal query performance:

```sql
-- For teams table
CREATE INDEX idx_teams_name ON teams(name);
CREATE INDEX idx_teams_code ON teams(code);

-- For matches table
CREATE INDEX idx_matches_date ON matches(date);
CREATE INDEX idx_matches_season ON matches(season);
CREATE INDEX idx_matches_home_team ON matches(home_team_id);
CREATE INDEX idx_matches_away_team ON matches(away_team_id);
CREATE INDEX idx_matches_teams ON matches(home_team_id, away_team_id);

-- For statistics table
CREATE INDEX idx_statistics_match ON statistics(match_id);
CREATE INDEX idx_statistics_team ON statistics(team_id);

-- For application tables
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_predictions_user ON predictions(user_id);
CREATE INDEX idx_predictions_match ON predictions(match_id);
CREATE INDEX idx_favorites_user ON favorites(user_id);
CREATE INDEX idx_favorites_team ON favorites(team_id);
```

### Query Optimization

Common queries that should be optimized:

```sql
-- Get team statistics for a specific match
SELECT * 
FROM statistics 
WHERE match_id = 123;

-- Get head-to-head history between two teams
SELECT m.*, 
       CASE WHEN m.home_team_id = 1 AND m.away_team_id = 2 THEN 'home'
            WHEN m.home_team_id = 2 AND m.away_team_id = 1 THEN 'away'
            ELSE NULL
       END as perspective
FROM matches m 
WHERE (m.home_team_id = 1 AND m.away_team_id = 2) 
   OR (m.home_team_id = 2 AND m.away_team_id = 1)
ORDER BY m.date DESC
LIMIT 10;

-- Get user's prediction history
SELECT p.*, t1.name as home_team, t2.name as away_team
FROM predictions p 
LEFT JOIN teams t1 ON p.home_team_id = t1.id
LEFT JOIN teams t2 ON p.away_team_id = t2.id
WHERE p.user_id = 123
ORDER BY p.created_at DESC;
```
