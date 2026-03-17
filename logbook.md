# Journal de Bord (Logbook) - Match Prediction App

Ce document retrace l'évolution du projet, les décisions techniques et les étapes d'implémentation.

## Étape 1 : Initialisation et Setup (17 Mars 2026)

### 1. Structure du projet et environnement
- Ajout du fichier `brief.md` détaillant les attentes du projet MVP IA entrepreneurial (FastAPI, DTOs, Validation, Tests).
- Création de l'environnement virtuel Python (`venv`) dans le dossier `FastAPI/`.
- Installation des dépendances principales : `fastapi`, `uvicorn`, `sqlalchemy`, `psycopg2-binary`, `python-jose[cryptography]`, `passlib[bcrypt]`, `pydantic`, `python-dotenv`, `httpx`, `pytest`, `pytest-asyncio`.
- Génération du fichier `requirements.txt` dans le dossier `FastAPI/`. (Nettoyage d'un `requirements.txt` en doublon à la racine).

### 2. Architecture de base de l'API (FastAPI)
- Création de la structure de l'application : `app/routers`, `app/schemas`, `app/models`, `app/services`, `app/middleware`.
- Création du point d'entrée `app/main.py` avec configuration initiale de l'application, ajout du middleware CORS (autorisant le futur front-end sur `localhost:3000`), et point de terminaison de santé (health_check).
- Mise en place des routeurs de base (`auth_router.py`, `prediction_router.py`, `user_router.py`) avec des endpoints de type "placeholder" pour l'instant.

### 3. Base de données et Modélisation
- Configuration de la connexion à la base de données PostgreSQL (`footballprediction_db`) via SQLAlchemy dans `app/database.py`.
- Stockage de l'URL de connexion dans un fichier `.env`.
- Traduction du Modèle Conceptuel de Données (MCD) SQL existant en modèles ORM SQLAlchemy dans `app/models/models.py`. Création des classes `Team`, `Match` et `TeamMatchStats` avec leurs relations respectives.
- Création des schémas Pydantic (`app/schemas/schemas.py`) pour la validation et la sérialisation des données correspondantes aux modèles.

---

## Étape 2 : Base de données Application & API Auth (17 Mars 2026)

### 1. Analyse du MCD existant
- Analyse du fichier `Data/MCD.sql` (`footballprediction_db`) : confirmation que ce schéma est destiné à l'**API ML/Data** (tables `team`, `match`, `team_match_stats` sont des features pour le modèle de classification).
- Décision : création d'une seconde base de données strictement séparée pour l'**API Application**.

### 2. Création du schéma de la DB Application
- Création du fichier `Data/MCD_app.sql` définissant la base `footballapp_db`.
- 3 tables créées :
  - `user` : gestion des comptes (username, email, hashed_password, is_active, created_at).
  - `prediction_history` : historique des prédictions par user (home/away team, predicted_result, confidence_score). Noms d'équipes en texte brut pour respecter la séparation inter-DB.
  - `user_favorite_team` : équipes favorites avec contrainte d'unicité (user_id, team_name).

### 3. Implémentation de l'API Application (FastAPI + JWT)
- Mise à jour du `FastAPI/.env` avec les URLs des deux bases de données (`DATABASE_APP_URL`, `DATABASE_ML_URL`) et les variables JWT.
- Création du service d'authentification `app/services/auth_service.py` : hashage des mots de passe (bcrypt), génération et vérification de tokens JWT (python-jose).
- Création des modèles SQLAlchemy pour la DB App dans `app/models/app_models.py` : `User`, `PredictionHistory`, `UserFavoriteTeam`.
- Création des schémas Pydantic pour l'API App dans `app/schemas/user_schemas.py` : DTOs pour Register, Login, réponse Token et User.
- Implémentation des routes dans `app/routers/auth_router.py` : `POST /auth/register`, `POST /auth/login`, `GET /auth/me`.
- Création du module `app/db_app.py` : moteur SQLAlchemy dédié à `footballapp_db`.

**Prochaines étapes prévues :**
- Développement des routes de prédiction (appel HTTP vers la ML API).
- Data Engineering : scripts d'ingestion multi-sources.

---

## Étape 3 : Séparation des APIs et refonte de l’architecture FastAPI (17 Mars 2026)

### 1. Problème identifié
- Le dossier historique `FastAPI/` mélangeait la logique de l’API Application (utilisateurs, historique) et de l’API ML (données de matchs) dans un seul projet FastAPI.
- Antigravity avait commencé à introduire `FastAPI_App/` et `FastAPI_ML/` sans y migrer réellement le code : on se retrouvait avec **3 dossiers** (`FastAPI/`, `FastAPI_App/`, `FastAPI_ML/`) et une architecture confuse.

### 2. Décision d’architecture
- Aligner le projet sur le plan d’implémentation : **2 APIs complètement séparées** avec chacune :
  - Son propre dossier (`FastAPI_App/`, `FastAPI_ML/`),
  - Son propre `requirements.txt`,
  - Son propre fichier `app/database.py` pointant vers la bonne base PostgreSQL,
  - Ses propres modèles, schémas, routes et services.
- Objectif : **séparation claire App / ML**, déploiement indépendant, et meilleure testabilité.

### 3. Mise en place de l’API Application (`FastAPI_App/`)
- Création du point d’entrée `FastAPI_App/app/main.py` :
  - Application FastAPI dédiée à l’App (titre, description, version).
  - Middleware CORS configuré pour le futur front-end.
  - Endpoint `/health` spécifique au service App.
  - Enregistrement centralisé des routes via `register_routes`.
- Création de `FastAPI_App/app/routes.py` :
  - Route racine `GET /` retournant un message d’accueil.
  - Fonction `register_routes(app)` pensée pour agréger à terme les routeurs d’authentification, d’utilisateurs et de prédictions.
- Migration des modèles de la DB Application :
  - Nouveau fichier `FastAPI_App/app/models.py` contenant `User`, `PredictionHistory`, `UserFavoriteTeam`.
  - Ces modèles réutilisent la structure définie dans `Data/MCD_app.sql` (gestion des utilisateurs, historique des prédictions et équipes favorites).
  - Les modèles sont reliés à `FastAPI_App/app/database.py` (base `footballapp_db` via `Base`).
- Migration et normalisation des schémas Pydantic pour l’App :
  - Création de `FastAPI_App/app/schemas/user.py` à partir de l’ancien `app/schemas/user_schemas.py` :
    - DTOs d’inscription (`UserRegister`) et de connexion (`UserLogin`).
    - Modèles de réponse pour les tokens (`Token`, `TokenData`) et le profil utilisateur (`UserOut`).
    - Modèle de sortie pour l’historique des prédictions (`PredictionHistoryOut`).
  - Création de `FastAPI_App/app/schemas/prediction.py` :
    - `PredictionRequest` (home_team_name, away_team_name).
    - `PredictionResponse` (predicted_result, confidence_score).
- Résultat : `FastAPI_App/` est désormais un projet FastAPI autonome centré sur l’API Application, prêt à accueillir la logique d’authentification et les appels HTTP vers l’API ML.

### 4. Mise en place de l’API ML (`FastAPI_ML/`)
- Création du point d’entrée `FastAPI_ML/app/main.py` :
  - Application FastAPI dédiée au service ML (titre, description, version).
  - Middleware CORS ouvert pour faciliter les appels inter-services.
  - Endpoint `/health` propre au service ML.
  - Enregistrement des routes via `register_routes`.
- Création de `FastAPI_ML/app/models.py` :
  - Migration des modèles `Team`, `Match`, `TeamMatchStats` depuis l’ancien `app/models/models.py`.
  - Connexion à la base `footballprediction_db` via `FastAPI_ML/app/database.py`.
  - Respect du schéma SQL décrit dans `Data/MCD.sql` (équipes, matchs, statistiques par équipe).
- Création de schémas Pydantic dédiés aux données de matchs :
  - `FastAPI_ML/app/schemas/team.py` : `TeamBase`, `TeamCreate`, `Team` pour sérialiser les équipes.
  - `FastAPI_ML/app/schemas/match.py` : `MatchBase`, `MatchCreate`, `Match` pour sérialiser les matchs.
- Mise en place d’un service ML minimal :
  - Nouveau fichier `FastAPI_ML/app/services/ml_service.py` avec une fonction `predict_match` qui renvoie pour l’instant un résultat **stub** (`DRAW` avec une confiance de `0.5`).
  - Ce stub servira de point d’ancrage à remplacer par un vrai pipeline scikit-learn (préprocessing, entraînement, sauvegarde, chargement).
- Création des routes de l’API ML :
  - Nouveau fichier `FastAPI_ML/app/routes.py` :
    - `GET /` : message de bienvenue pour l’API ML.
    - `POST /predict` : route de prédiction qui appelle `ml_service.predict_match` (structure compatible avec une évolution vers un vrai modèle).

### 5. Gestion des anciens fichiers et prochaine étape de nettoyage
- Le dossier historique `FastAPI/` contient encore l’ancienne application monolithique (mélange App + ML).
- Toute la logique utile a été recopiée et structurée dans :
  - `FastAPI_App/` pour la partie Application.
  - `FastAPI_ML/` pour la partie ML.
- **Décision** : le dossier `FastAPI/` est désormais obsolète et sera supprimé du projet (et ignoré par Git) une fois les tests de démarrage des deux nouvelles APIs validés.
- Chaque API disposera de son environnement virtuel dédié (`venv` séparé) et de son propre fichier `requirements.txt`, ce qui facilite le déploiement indépendant et la maintenance.

