CREATE DATABASE footballprediction_db;

\c footballprediction_db;

-- Table des équipes
CREATE TABLE team (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

-- Table des matchs
CREATE TABLE match (
  id SERIAL PRIMARY KEY,
  date TIMESTAMP NOT NULL,
  home_team_id INT NOT NULL,
  away_team_id INT NOT NULL,
  home_score INT,
  away_score INT,
  result VARCHAR(10),
  CONSTRAINT fk_home_team FOREIGN KEY (home_team_id) REFERENCES team (id) DEFERRABLE INITIALLY IMMEDIATE,
  CONSTRAINT fk_away_team FOREIGN KEY (away_team_id) REFERENCES team (id) DEFERRABLE INITIALLY IMMEDIATE
);

-- Table des stats par équipe pour chaque match
CREATE TABLE team_match_stats (
  id SERIAL PRIMARY KEY,
  match_id INT NOT NULL,
  team_id INT NOT NULL,
  is_home BOOLEAN,
  goals INT,
  shots INT,
  shots_on_target INT,
  yellow_cards INT,
  red_cards INT,
  corners INT,
  fouls INT,
  CONSTRAINT fk_team FOREIGN KEY (team_id) REFERENCES team (id) DEFERRABLE INITIALLY IMMEDIATE,
  CONSTRAINT fk_match FOREIGN KEY (match_id) REFERENCES match (id) DEFERRABLE INITIALLY IMMEDIATE
);