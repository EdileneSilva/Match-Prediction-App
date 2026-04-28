-- Tables pour la base de données footballapp_db
-- Connexion à la base de données footballapp_db
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
