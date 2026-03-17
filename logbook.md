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

**Prochaines étapes prévues :**
- Développement des routes (Endpoints) fonctionnelles avec intégration de la base de données.
- Développement du script de scraping ou d'ingestion de données (Data Engineering).
