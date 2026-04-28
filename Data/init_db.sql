-- Script d'initialisation simplifié pour PostgreSQL
-- Crée les bases de données et tables si elles n'existent pas déjà

-- Création de la base de données footballapp_db
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'footballapp_db') THEN
        CREATE DATABASE footballapp_db;
    END IF;
END
$$;

-- Création de la base de données footballprediction_db
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'footballprediction_db') THEN
        CREATE DATABASE footballprediction_db;
    END IF;
END
$$;

-- Connexion à footballapp_db et création des tables
\c footballapp_db

-- Table des équipes
CREATE TABLE IF NOT EXISTS teams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    logo_url VARCHAR(255)
);

-- Table des utilisateurs
CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Table de l'historique des prédictions
CREATE TABLE IF NOT EXISTS prediction_history (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    home_team_name VARCHAR(100) NOT NULL,
    away_team_name VARCHAR(100) NOT NULL,
    predicted_result VARCHAR(10),
    confidence_score NUMERIC(5, 4),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_user_prediction FOREIGN KEY (user_id)
        REFERENCES "user" (id) ON DELETE CASCADE
);

-- Table des équipes favorites
CREATE TABLE IF NOT EXISTS user_favorite_team (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    team_id INT,
    CONSTRAINT fk_user_favorite FOREIGN KEY (user_id)
        REFERENCES "user" (id) ON DELETE CASCADE,
    CONSTRAINT fk_team_favorite FOREIGN KEY (team_id)
        REFERENCES teams (id),
    CONSTRAINT uq_user_team UNIQUE (user_id, team_id)
);

-- Connexion à footballprediction_db et création des tables
\c footballprediction_db

-- Table des équipes
CREATE TABLE IF NOT EXISTS teams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Table des matchs
CREATE TABLE IF NOT EXISTS football_matches (
    id SERIAL PRIMARY KEY,
    league_season INT NOT NULL,
    home_team_id INT NOT NULL,
    away_team_id INT NOT NULL,
    home_score INT,
    away_score INT,
    date VARCHAR(50),
    time VARCHAR(20),
    result VARCHAR(10),
    halftime_home_goals INT,
    halftime_away_goals INT,
    halftime_result VARCHAR(10),
    home_shot INT,
    away_shot INT,
    home_shot_target INT,
    away_shot_target INT,
    home_team_fouls INT,
    away_team_fouls INT,
    home_team_corners INT,
    away_team_corners INT,
    home_yellow_cards INT,
    away_yellow_cards INT,
    home_red_cards INT,
    away_red_cards INT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT fk_home_team FOREIGN KEY (home_team_id)
        REFERENCES teams (id) ON DELETE RESTRICT,
    CONSTRAINT fk_away_team FOREIGN KEY (away_team_id)
        REFERENCES teams (id) ON DELETE RESTRICT
);

-- Table des statistiques de matchs
CREATE TABLE IF NOT EXISTS match_stats (
    id SERIAL PRIMARY KEY,
    match_id INT NOT NULL UNIQUE,
    home_goals_scored_home FLOAT,
    home_goals_conceded_home FLOAT,
    home_win_rate_home FLOAT,
    away_goals_scored_away FLOAT,
    away_goals_conceded_away FLOAT,
    away_win_rate_away FLOAT,
    home_season_rank INT,
    away_season_rank INT,
    home_rolling_scored FLOAT,
    home_rolling_conceded FLOAT,
    home_rolling_win_rate FLOAT,
    away_rolling_scored FLOAT,
    away_rolling_conceded FLOAT,
    away_rolling_win_rate FLOAT,
    CONSTRAINT fk_match_stats FOREIGN KEY (match_id)
        REFERENCES football_matches (id) ON DELETE CASCADE
);

-- Table des statistiques d'équipes
CREATE TABLE IF NOT EXISTS team_stats_reference (
    id SERIAL PRIMARY KEY,
    team VARCHAR(100) NOT NULL,
    season INT NOT NULL,
    goals_scored_home FLOAT,
    goals_conceded_home FLOAT,
    win_rate_home FLOAT,
    goals_scored_away FLOAT,
    goals_conceded_away FLOAT,
    win_rate_away FLOAT,
    season_rank FLOAT,
    rolling_scored_home FLOAT,
    rolling_conceded_home FLOAT,
    rolling_win_rate_home FLOAT,
    rolling_scored_away FLOAT,
    rolling_conceded_away FLOAT,
    rolling_win_rate_away FLOAT,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT uq_team_season UNIQUE (team, season)
);

-- Table des logs d'entraînement
CREATE TABLE IF NOT EXISTS train_log (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    model_version VARCHAR(50) NOT NULL,
    n_samples INT NOT NULL,
    cv_accuracy FLOAT NOT NULL,
    cv_log_loss FLOAT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'success',
    error_message VARCHAR(500)
);
