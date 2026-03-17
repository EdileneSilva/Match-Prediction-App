CREATE TABLE "Team" (
  "id" int PRIMARY KEY,
  "name" varchar
);

CREATE TABLE "Match" (
  "id" int PRIMARY KEY,
  "date" datetime,
  "home_team_id" int,
  "away_team_id" int,
  "home_score" int,
  "away_score" int,
  "result" varchar
);

CREATE TABLE "TeamMatchStats" (
  "id" int PRIMARY KEY,
  "match_id" int,
  "team_id" int,
  "is_home" boolean,
  "goals" int,
  "shots" int,
  "shots_on_target" int,
  "yellow_cards" int,
  "red_cards" int,
  "corners" int,
  "fouls" int
);

ALTER TABLE "TeamMatchStats" ADD FOREIGN KEY ("team_id") REFERENCES "Team" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "TeamMatchStats" ADD FOREIGN KEY ("match_id") REFERENCES "Match" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "Match" ADD FOREIGN KEY ("home_team_id") REFERENCES "Team" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "Match" ADD FOREIGN KEY ("away_team_id") REFERENCES "Team" ("id") DEFERRABLE INITIALLY IMMEDIATE;
