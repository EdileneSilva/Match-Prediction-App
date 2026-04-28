![Match Prediction App](docs/match-prediction-banner.jpg)

# Match Prediction App

Application complète de prédiction de matchs de Ligue 1 :

- **2 APIs FastAPI** séparées — Application & ML
- **2 bases PostgreSQL** — `footballapp_db` (users/historique) & `footballprediction_db` (matchs/stats)
- **1 frontend Vue 3** avec GSAP + Lenis
- **1 pipeline ML** scikit-learn + MLflow (ingestion, entraînement, prédiction)
- **1 scraper LFP** pour les données live (matchs, classement, buteurs)

---

## Architecture

```
┌──────────────────┐       ┌──────────────────┐
│   Vue 3 Frontend │──────▶│   API App :8000  │
│  localhost:8080   │       │ auth, history,   │
└──────────────────┘       │ dashboard, proxy │
        │                  └────────┬─────────┘
        │                           │ proxy /predict
        ▼                           ▼
┌──────────────────┐       ┌──────────────────┐
│  API LFP (ext.)  │       │   API ML :8001   │
│  scraper live    │       │ train, predict,  │
└──────────────────┘       │ ingestion        │
                           └────────┬─────────┘
                                    │
                           ┌────────▼─────────┐
                           │  PostgreSQL :5432 │
                           │ footballapp_db    │
                           │ footballprediction│
                           │        _db       │
                           └──────────────────┘
```

---

## Pré-requis

| Outil | Version |
|-------|---------|
| Python | 3.12+ |
| Node.js | 18+ et npm |
| PostgreSQL | 15+ (accès superuser) |
| Docker + Compose | _(optionnel)_ |

---

## Installation locale

### Configuration (.env)

Un **seul fichier `.env`** à la racine, lu par les deux APIs via `shared/config/base_settings.py` :

```sh
cp .env.example .env
```

```env
# --- Bases de données ---
DATABASE_APP_URL=postgresql://postgres:postgres@localhost:5432/footballapp_db
DATABASE_ML_URL=postgresql://postgres:postgres@localhost:5432/footballprediction_db

# --- Auth JWT (API Application) ---
SECRET_KEY=change-me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# --- MLflow ---
MLFLOW_TRACKING_URI=sqlite:///mlflow.db
```

### Bases de données

```sh
psql -U postgres -f Data/MCD.sql        # footballprediction_db (ML)
psql -U postgres -f Data/MCD_app.sql    # footballapp_db (Application)
```

> Avec Docker, les bases sont créées automatiquement via `create_databases.sql`, `create_tables_app.sql`, `create_tables_ml.sql`.

---

## API Application — `FastAPI_App`

**Port** : `8000` | **Docs** : http://localhost:8000/docs

### Fonctionnalités

- Auth JWT complète : register, login, forgot/reset password, changement de mot de passe
- CRUD utilisateur : profil, suppression de compte, statistiques
- Équipes favorites : ajout/suppression/liste
- Historique des prédictions avec enrichissement live (résultats réels via API LFP, score de proximité)
- Dashboard live : prochains matchs, classement Ligue 1, statistiques buts (scraper LFP)
- Proxy vers l'API ML pour les prédictions
- Seeding automatique de 18 équipes Ligue 1 au démarrage

### Installation & lancement

```sh
cd FastAPI_App
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

```sh
curl http://127.0.0.1:8000/health
# -> {"status":"ok","service":"app-api"}
```

### Dépendances clés

`fastapi`, `uvicorn`, `SQLAlchemy`, `psycopg2-binary`, `passlib[bcrypt]`, `python-jose[cryptography]`, `pydantic[email]`, `httpx`, `pydantic-settings`, `requests`

---

## API ML — `FastAPI_ML`

**Port** : `8001` | **Docs** : http://localhost:8001/docs

### Fonctionnalités

- Ingestion de données CSV en base (`POST /ingest`)
- Entraînement du modèle avec MLflow tracking (`POST /train`, `GET /train/history`)
- Prédiction de résultat avec probabilités (`POST /predict`)
- Liste des équipes (`GET /teams`)
- Chargement automatique du modèle au démarrage si `match_model_v1.joblib` existe

### Installation & lancement

```sh
cd FastAPI_ML
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

```sh
curl http://127.0.0.1:8001/health
# -> {"status":"ok","service":"ml-api"}
```

### Première utilisation (modèle non pré-entraîné)

```sh
# 1. Ingestion des données de base
curl -X POST http://localhost:8001/ingest

# 2. Entraînement du modèle
curl -X POST http://localhost:8001/train
```

### Dépendances clés

`fastapi`, `uvicorn`, `SQLAlchemy`, `psycopg2-binary`, `pandas`, `numpy`, `scikit-learn`, `mlflow`, `scipy`, `pydantic-settings`

---

## Frontend Vue.js — `match_prediction_app-front`

**Port** : `8080` | Consomme les deux APIs via `src/api/client.js`

### Pages (routes)

| Route | Vue | Accès |
|-------|-----|-------|
| `/` | LandingView | guest only |
| `/dashboard` | HomeView | auth required |
| `/predictions` | PredictionView | auth required |
| `/history` | HistoryView | auth required |
| `/statistics` | StatisticsView | auth required |
| `/profile` | ProfileView | auth required |
| `/login` | LoginView | guest only |
| `/register` | RegisterView | guest only |
| `/forgot-password` | ForgotView | guest only |
| `/reset-password` | ResetView | guest only |
| `/exit` | — | déconnexion + redirect `/login` |

### Installation & lancement

```sh
cd match_prediction_app-front
npm install
npm run serve
```

### Flux d'authentification

- `POST /auth/login` → token JWT stocké dans `localStorage`
- `src/api/client.js` ajoute automatiquement `Authorization: Bearer <token>`
- Le routeur Vue protège les pages via `meta.requiresAuth` / `meta.guestOnly`
- Sans token → redirection vers `/login`

### Dépendances clés

`vue@3`, `vue-router@4`, `gsap`, `lenis`, `split-type`

---

## Docker

Lancer l'ensemble avec une seule commande (voir `DOCKER_QUICKSTART.md` pour le détail) :

```sh
cp .env.example .env
docker compose up -d --build
```

| Conteneur | Service | URL |
|-----------|---------|-----|
| `frontend_container` | Vue 3 Frontend | http://localhost:8080 |
| `fastapi_app_container` | API App | http://localhost:8000/docs |
| `fastapi_ml_container` | API ML | http://localhost:8001/docs |
| `postgres_db` | PostgreSQL | `localhost:5432` |

Première utilisation avec Docker :

```sh
curl -X POST http://localhost:8001/ingest
curl -X POST http://localhost:8001/train
```

---

## API Reference

### API App (`:8000`)

| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| POST | `/auth/register` | Créer un compte | ❌ |
| POST | `/auth/login` | Connexion → JWT | ❌ |
| GET | `/auth/me` | Profil courant | ✅ |
| PUT | `/auth/me` | Modifier le profil | ✅ |
| DELETE | `/auth/me` | Supprimer le compte | ✅ |
| POST | `/auth/change-password` | Changer le mot de passe | ✅ |
| POST | `/auth/forgot-password` | Demander un reset | ❌ |
| POST | `/auth/reset-password` | Réinitialiser mot de passe | ❌ |
| GET | `/auth/me/stats` | Stats utilisateur | ✅ |
| GET | `/auth/me/favorites` | Équipes favorites | ✅ |
| POST | `/auth/me/favorites` | Ajouter un favori | ✅ |
| DELETE | `/auth/me/favorites/{team_id}` | Supprimer un favori | ✅ |
| GET | `/predictions/teams` | Liste des équipes | ❌ |
| POST | `/predictions/predict` | Prédiction (proxy ML) | ✅ |
| GET | `/predictions/history` | Historique prédictions | ✅ |
| POST | `/predictions/history` | Sauvegarde manuelle | ✅ |
| GET | `/dashboard/upcoming` | Prochains matchs LFP | ❌ |
| GET | `/dashboard/standings` | Classement Ligue 1 | ❌ |
| GET | `/dashboard/goals-stats` | Stats buts Ligue 1 | ❌ |
| GET | `/health` | Healthcheck | ❌ |

### API ML (`:8001`)

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/teams` | Liste des équipes |
| POST | `/predict` | Prédiction d'un match |
| POST | `/train` | Entraîner le modèle |
| GET | `/train/history` | Historique entraînements |
| POST | `/ingest` | Ingestion de données (CSV optionnel) |
| GET | `/health` | Healthcheck |

---

## Modèle ML & Features

### Pipeline

1. **Ingestion** (`PreparationService`) — nettoyage et insertion des CSV en base
2. **Feature Engineering** — calcul de `match_stats` et `team_stats_reference` (buts, win rate, classement, rolling averages)
3. **Entraînement** (`PipelineService`) — RandomForestClassifier + CalibratedClassifierCV, StandardScaler, OneHotEncoder, cross-validation, logging MLflow
4. **Prédiction** (`MLService`) — chargement du modèle joblib, construction des features, `predict_proba`

### Features (15 numériques + 2 catégorielles)

| Feature | Description |
|---------|-------------|
| `home_goals_scored_home` | Buts marqués à domicile (saison) |
| `home_goals_conceded_home` | Buts encaissés à domicile (saison) |
| `home_win_rate_home` | Taux de victoire à domicile |
| `away_goals_scored_away` | Buts marqués à l'extérieur (saison) |
| `away_goals_conceded_away` | Buts encaissés à l'extérieur (saison) |
| `away_win_rate_away` | Taux de victoire à l'extérieur |
| `home_season_rank` | Classement équipe domicile |
| `away_season_rank` | Classement équipe extérieur |
| `home_rolling_scored` | Moyenne mobile buts marqués (5 derniers) |
| `home_rolling_conceded` | Moyenne mobile buts encaissés (5 derniers) |
| `home_rolling_win_rate` | Moyenne mobile win rate (5 derniers) |
| `away_rolling_scored` | Moyenne mobile buts marqués (5 derniers) |
| `away_rolling_conceded` | Moyenne mobile buts encaissés (5 derniers) |
| `away_rolling_win_rate` | Moyenne mobile win rate (5 derniers) |
| `league_season` | Saison |
| `HomeTeam` | Nom équipe domicile (catégorielle) |
| `AwayTeam` | Nom équipe extérieur (catégorielle) |

### Résultat de prédiction

```json
{
  "match": "Paris SG vs Marseille",
  "prediction": "HOME_WIN",
  "confidence": 0.5421,
  "probabilities": {
    "HOME": 0.5421,
    "DRAW": 0.2613,
    "AWAY": 0.1966
  }
}
```

---

## Tests

### API App

```sh
cd FastAPI_App
source venv/bin/activate
pytest tests/ -v
```

Tests : `test_auth.py`, `test_auth_routes.py`, `test_auth_service.py`, `test_dashboard.py`, `test_predictions.py`

### Frontend

```sh
cd match_prediction_app-front
npm run test:unit
npm run test:coverage
```

---

## Structure du projet

```
Match-Prediction-App/
├── FastAPI_App/                  # API Application (port 8000)
│   ├── app/
│   │   ├── core/config.py
│   │   ├── models/              # User, PredictionHistory, UserFavoriteTeam, Team
│   │   ├── routes/              # auth, prediction, dashboard
│   │   ├── schemas/             # user, prediction
│   │   ├── services/auth_service.py
│   │   ├── utils/               # scraper_ligue1, team_mapper
│   │   ├── database.py
│   │   └── main.py
│   ├── tests/
│   ├── Dockerfile.api
│   └── requirements.txt
├── FastAPI_ML/                   # API ML (port 8001)
│   ├── app/
│   │   ├── core/config.py
│   │   ├── models/              # Team, FootballMatch, MatchStats, TeamStatsReference, TrainLog
│   │   ├── routes/              # predict, train, ingestion
│   │   ├── schemas/             # match, request, team
│   │   ├── services/            # ml_service, pipeline, preparation
│   │   ├── database.py
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── match_prediction_app-front/   # Frontend Vue 3 (port 8080)
│   ├── src/
│   │   ├── api/client.js        # Client HTTP (routing App/ML)
│   │   ├── views/               # 10 vues (Landing, Login, Register, etc.)
│   │   ├── components/          # NavigationBar, dashboard/, landing/
│   │   ├── router/index.js
│   │   └── services/
│   ├── Dockerfile
│   └── package.json
├── Data/                         # Données & SQL
│   ├── MCD.sql / MCD_app.sql    # Schémas BDD complets
│   ├── create_databases.sql
│   ├── create_tables_app.sql
│   ├── create_tables_ml.sql
│   └── dataset/                 # CSV + modèle joblib
├── shared/                       # Config commune
│   └── config/base_settings.py   # CommonSettings (pydantic)
├── notebooks/                    # Exploration ML (Jupyter)
├── docker-compose.yml
├── .env.example
└── DOCKER_QUICKSTART.md
```