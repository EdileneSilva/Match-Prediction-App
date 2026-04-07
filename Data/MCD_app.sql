-- ============================================================
-- DB APPLICATION : footballapp_db
-- Gestion des utilisateurs, de l'authentification et de
-- l'historique des predictions.
-- SEPAREE de footballprediction_db (DB ML / Data).
-- ============================================================

CREATE DATABASE footballapp_db;

\c footballapp_db;

-- ============================================================
-- Table des utilisateurs (authentification JWT)
-- ============================================================
CREATE TABLE "user" (
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
CREATE TABLE prediction_history (
    id               SERIAL        PRIMARY KEY,
    user_id          INT           NOT NULL,
    home_team_id     INTEGER       NOT NULL,
    away_team_id     INTEGER       NOT NULL,
    home_team_name   VARCHAR(100)  NOT NULL,  -- AJOUTER
    away_team_name   VARCHAR(100)  NOT NULL,  -- AJOUTER
    predicted_result VARCHAR(10),
    confidence_score NUMERIC(5, 4),
    created_at       TIMESTAMP     NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_user_prediction FOREIGN KEY (user_id)
        REFERENCES "user" (id) ON DELETE CASCADE,
    CONSTRAINT fk_home_team FOREIGN KEY (home_team_id)
        REFERENCES teams(id) ON DELETE CASCADE,
    CONSTRAINT fk_away_team FOREIGN KEY (away_team_id)
        REFERENCES teams(id) ON DELETE CASCADE
);

-- Créer la table teams
CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    logo_url VARCHAR(255)
);

 

-- ============================================================
-- Table des equipes favorites d'un utilisateur
-- ============================================================
CREATE TABLE user_favorite_team (
    id        SERIAL       PRIMARY KEY,
    user_id   INT          NOT NULL,
    team_id   INTEGER      NOT NULL,
    CONSTRAINT fk_user_favorite FOREIGN KEY (user_id)
        REFERENCES "user" (id) ON DELETE CASCADE,
    CONSTRAINT fk_team FOREIGN KEY (team_id)
        REFERENCES teams(id) ON DELETE CASCADE,
    CONSTRAINT uq_user_team UNIQUE (user_id, team_id)
);