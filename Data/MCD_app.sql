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