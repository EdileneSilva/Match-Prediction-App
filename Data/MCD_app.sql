-- ============================================================
-- DB APPLICATION : footballapp_db
-- Gestion des utilisateurs, de l'authentification et de
-- l'historique des predictions.
-- SEPAREE de footballprediction_db (DB ML / Data).
-- ============================================================

SELECT 'CREATE DATABASE footballapp_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'footballapp_db')\gexec
-- ============================================================
-- DB APPLICATION : footballapp_db
-- Gestion des utilisateurs, de l'authentification et de
-- l'historique des predictions.
-- SEPAREE de footballprediction_db (DB ML / Data).
-- ============================================================

SELECT 'CREATE DATABASE footballapp_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'footballapp_db')\gexec

\c footballapp_db;

-- ============================================================
-- Table des équipes (référence pour les prédictions)
-- ============================================================
CREATE TABLE IF NOT EXISTS teams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    logo_url VARCHAR(255)
);

-- ============================================================
-- Table des utilisateurs (authentification JWT)
-- ============================================================
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================================================
-- Table de l'historique des predictions
-- Corrigée pour correspondre au modèle SQLAlchemy
-- ============================================================
CREATE TABLE prediction_history (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    home_team_id INT NOT NULL,
    away_team_id INT NOT NULL,
    home_team_name VARCHAR(100) NOT NULL,
    home_team_logo_url TEXT,
    away_team_name VARCHAR(100) NOT NULL,
    away_team_logo_url TEXT,
    predicted_result VARCHAR(10),
    confidence_score NUMERIC(5, 4),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_user_prediction FOREIGN KEY (user_id)
        REFERENCES "user" (id) ON DELETE CASCADE,
    CONSTRAINT fk_home_team FOREIGN KEY (home_team_id)
        REFERENCES teams (id),
    CONSTRAINT fk_away_team FOREIGN KEY (away_team_id)
        REFERENCES teams (id)
);

-- ============================================================
-- Table des équipes favorites d'un utilisateur
-- Corrigée pour utiliser team_id au lieu de team_name
-- ============================================================
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

-- Index pour optimiser les performances
CREATE INDEX idx_prediction_history_user_id ON prediction_history(user_id);
CREATE INDEX idx_prediction_history_created_at ON prediction_history(created_at);
CREATE INDEX idx_user_favorite_team_user_id ON user_favorite_team(user_id);
\c footballapp_db;

-- ============================================================
-- Table des utilisateurs (authentification JWT)
-- ============================================================
CREATE TABLE IF NOT EXISTS "user" (
    id              SERIAL       PRIMARY KEY,
    username        VARCHAR(50)  NOT NULL UNIQUE,
    email           VARCHAR(100) NOT NULL UNIQUE,
    hashed_password TEXT         NOT NULL,
    is_active       BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMP    NOT NULL DEFAULT NOW()
);

-- ============================================================
-- Table de l'historique des predictions
-- Stocke les resultats demandes par chaque utilisateur.
-- Les noms d'equipes sont en texte brut (pas de FK inter-DB).
-- L'App API communique avec la ML API via HTTP, pas via SQL.
-- ============================================================
CREATE TABLE IF NOT EXISTS prediction_history (
    id               SERIAL        PRIMARY KEY,
    user_id          INT           NOT NULL,
    home_team_name   VARCHAR(100)  NOT NULL,
    away_team_name   VARCHAR(100)  NOT NULL,
    predicted_result VARCHAR(10),
    confidence_score NUMERIC(5, 4),
    created_at       TIMESTAMP     NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_user_prediction FOREIGN KEY (user_id)
        REFERENCES "user" (id) ON DELETE CASCADE
);

-- ============================================================
-- Table des equipes favorites d'un utilisateur
-- ============================================================
CREATE TABLE user_favorite_team (
    id        SERIAL       PRIMARY KEY,
    user_id   INT          NOT NULL,
    team_name VARCHAR(100) NOT NULL,
    CONSTRAINT fk_user_favorite FOREIGN KEY (user_id)
        REFERENCES "user" (id) ON DELETE CASCADE,
    CONSTRAINT uq_user_team UNIQUE (user_id, team_name)
);