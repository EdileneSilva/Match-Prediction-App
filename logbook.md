# Logbook - Match Prediction App

---

## Sprint actuel — Branche `feature/tests` (27 mars 2026)

### 🧪 Suite de tests complète (37 tests — 100% passed)

**FastAPI_App (34 tests)**

- `test_auth_routes.py` : Tests fonctionnels de toutes les routes `/auth/*` (inscription, login, profil, favoris, mot de passe, stats)
- `test_auth_service.py` : Tests unitaires de la logique métier d'authentification
- `test_prediction_flow.py` : Tests d'intégration du flux de prédiction (mapping ID→Nom, 401 sans token, erreur ML 503)
- `test_e2e_scenarios.py` : Scénario complet — Inscription → Login → Prédiction → Historique → Stats

**FastAPI_ML (3 tests)**

- Health check, prédiction valide, validation des champs requis

### 🔐 Authentification réactivée

- Les routes `/predictions/predict` et `/predictions/history` requièrent un token JWT
- L'historique est désormais **isolé par utilisateur** (fin du `user_id=1` hardcodé)

### 🐛 Corrections

- Migration PostgreSQL → SQLite en mémoire pour l'isolation des tests
- `bcrypt` downgradé en `4.0.1` pour compatibilité avec `passlib`

---

### Dernière Session (Documentation & Tests)
**Objectif**: Réécrire le README pour une installation en < 15 min, enrichir la documentation Swagger OpenAPI, et intégrer la suite de tests complète (37 tests).
- Création de la branche `docs/readme-and-api`
- Réécriture exhaustive du `README.md`
- Documentation de tous les endpoints dans `FastAPI_App` et `FastAPI_ML` via Swagger (`tags_metadata`, descriptions explicites)
- Fusion de la branche `feature/tests` et validation locale avec DB en mémoire (`sqlite:///:memory:`)
- Push de la branche sur GitHub et génération de la description pour la Pull Request

### Sprint M (Sécurité, CI/CD, Déploiement) — Branche `data/seed-teams` (27 mars 2026)

### ☁️ Migration PostgreSQL

- Deux bases distinctes : `footballapp_db` (FastAPI_App) et `footballml_db` (FastAPI_ML)
- Mise à jour des `DATABASE_URL` dans les `config.py`

### ⚽ Équipes Ligue 1

- Modèle `Team` avec `name`, `short_name`, `logo_url`
- Script `seed_teams.py` + service statique pour les logos (`/static/logos/`)

### 🔁 Standardisation API

- Champs uniformisés : `prediction` et `confidence` partout (App + ML + Frontend)
- `FastAPI_App` agit comme proxy métier : reçoit des IDs, mappe vers des noms, appelle le ML

---

# Logbook - Feature: Futuristic Landing Page & Team Dev Access

Ce logbook résume les modifications apportées à la branche `feature/futuristic-landing-page` pour optimiser le pipeline de prédiction et permettre un accès de développement facilité pour l'équipe.

## 🚀 Modifications Apportées

### 1. Intelligence Artificielle (Pipeline v3)
- **Modèle Ensemble (Stacking)** : Intégration d'un modèle de Stacking combinant **Random Forest**, **XGBoost** et **Logistic Regression**.
- **Calibration des Probabilités** : Utilisation de `CalibratedClassifierCV` pour des probabilités plus fiables (Accuracy: 57.55%, Log Loss: 0.9299).
- **Market Intelligence** : Utilisation des cotes moyennes de paris comme indicateurs de force des équipes.

### 2. Accès de Développement (Auth Bypass)
- **Frontend** : 
    - Bypass du middleware d'authentification dans `src/router/index.js`.
    - Ajout de liens directs vers "Prédictions" et "Historique" dans la `NavBar` pour une navigation sans compte.
    - Correction de bug dans `HistoryView.vue` (gestion des détails et calculs de stats).
- **Backend (FastAPI_App & FastAPI_ML)** :
    - Suppression temporaire des dépendances `get_current_user` sur les routes de prédiction et d'historique.
    - Configuration CORS mise à jour pour le développement local.

### 3. Transition vers SQLite (Zero Config)
- **Migration PostgreSQL -> SQLite** : Passage temporaire à SQLite pour supprimer la dépendance à un serveur Postgres externe.
- **Auto-Initialization** : Création automatique des tables au démarrage si elles n'existent pas.
- **Seeding Automatique** : Création d'un utilisateur par défaut (`id=1`) et chargement automatique de la liste des équipes de Premier League dans la base de données ML au lancement.

---

## 🛠️ Instructions de Lancement

Pour lancer l'environnement complet, ouvrez **3 terminaux séparés** :

### Terminal 1 : Backend API (Main)
```bash
cd FastAPI_App
python3 -m uvicorn app.main:app --port 8000 --reload
```
*Note : Utilise la base `FastAPI_App/app.db`.*

### Terminal 2 : Moteur ML (Intelligence Engine)
```bash
cd FastAPI_ML
python3 -m uvicorn app.main:app --port 8001 --reload
```
*Note : Utilise la base `FastAPI_ML/ml_app.db`.*

### Terminal 3 : Frontend (Vue.js)
```bash
cd match_prediction_app-front
npm run serve
```
*Accès : http://localhost:8080*

---

## 🛡️ Rappels de Sécurité
> [!WARNING]
> Ces modifications sont strictement destinées au développement et aux tests internes. L'authentification est désactivée. Avant de fusionner sur `main`, il est impératif de restaurer la sécurité et les configurations PostgreSQL.
