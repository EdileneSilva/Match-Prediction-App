![Match Prediction App](docs/match-prediction-banner.jpg)

# Match Prediction App

Application complète de prédiction de matchs de Ligue 1 avec :
- 2 APIs FastAPI séparées (Application & ML)
- 2 bases PostgreSQL séparées (`footballapp_db` & `footballml_db`)
- 1 frontend Vue.js 3
- Migrations de base de données versionnées avec **Alembic**

---

## Architecture

```
Match-Prediction-App/
├── FastAPI_App/          # API Application (auth, historique, favoris)
│   ├── alembic/          # Migrations de footballapp_db
│   ├── alembic.ini
│   └── app/
├── FastAPI_ML/           # API ML (matchs, entraînement, prédiction)
│   ├── alembic/          # Migrations de footballml_db
│   ├── alembic.ini
│   └── app/
├── Data/
│   ├── MCD_app.sql       # Référence du schéma App (documentation)
│   ├── MCD.sql           # Référence du schéma ML (documentation)
│   └── seeds/
│       └── teams_seed.sql  # Seeding initial des équipes (optionnel)
├── match_prediction_app-front/
├── .env.example          # Template de configuration (à copier en .env)
└── .env                  # NON commité — variables locales
```

> **Règle d'équipe :** toute modification du schéma de base de données
> passe obligatoirement par une migration Alembic. Ne jamais modifier
> les tables directement en SQL.

---

## 1. Pré-requis

- Python 3.12+
- Node.js 18+ et npm
- PostgreSQL installé et en cours d'exécution (port 5432)

---

## 2. Configuration (.env)

```sh
# À la racine du projet
cp .env.example .env
```

Édite `.env` avec tes vraies valeurs :

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/footballapp_db
DATABASE_ML_URL=postgresql://postgres:postgres@localhost:5432/footballml_db
SECRET_KEY=<génère avec: openssl rand -hex 32>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
ML_API_URL=http://localhost:8001
MODEL_PATH=../Data/dataset/match_model_v1.joblib
DATASET_PATH=../Data/dataset/completed_match_dataset_final.csv
DATA_DIR=../Data
```

---

## 3. Setup base de données (nouvelle installation)

### 3.1 Créer les bases PostgreSQL

```sh
psql -U postgres -c "CREATE DATABASE footballapp_db;"
psql -U postgres -c "CREATE DATABASE footballml_db;"
```

### 3.2 Appliquer les migrations (crée toutes les tables)

```sh
# Base Application
cd FastAPI_App
source venv/bin/activate
alembic upgrade head

# Base ML
cd ../FastAPI_ML
source venv/bin/activate
alembic upgrade head
```

### 3.3 Seeder les équipes (optionnel)

```sh
psql -U postgres -d footballapp_db -f Data/seeds/teams_seed.sql
```

---

## 4. Setup base de données (reprise sur base existante)

Si tu clones le projet alors que la base existe déjà (migration depuis l'ancien système) :

```sh
# Synchroniser Alembic avec l'état actuel de la base (sans modifier les données)
cd FastAPI_App
source venv/bin/activate
alembic stamp head

cd ../FastAPI_ML
source venv/bin/activate
alembic stamp head
```

---

## 5. API Application – `FastAPI_App`

### Environnement virtuel & dépendances

```sh
cd FastAPI_App
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Lancement

```sh
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Vérification :

```sh
curl http://127.0.0.1:8000/health
# → {"status":"ok","service":"app-api"}
```

---

## 6. API ML – `FastAPI_ML`

### Environnement virtuel & dépendances

```sh
cd FastAPI_ML
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Lancement

```sh
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

Vérification :

```sh
curl http://127.0.0.1:8001/health
# → {"status":"ok","service":"ml-api"}
```

---

## 7. Frontend Vue.js – `match_prediction_app-front`

### Installation & lancement

```sh
cd match_prediction_app-front
npm install
npm run serve
```

Ouvre ensuite l'URL affichée (généralement `http://localhost:8080`).

---

## 8. Workflow de migration Alembic (équipe)

### Créer une nouvelle migration (après modification d'un modèle SQLAlchemy)

```sh
cd FastAPI_App  # ou FastAPI_ML
source venv/bin/activate
alembic revision --autogenerate --message "description_du_changement"
# Vérifier le fichier généré dans alembic/versions/
alembic upgrade head
```

> ⚠️ Toujours **relire le fichier de migration généré** avant de l'appliquer.
> L'autogenerate peut parfois produire des opérations inattendues.

### Revenir en arrière

```sh
alembic downgrade -1  # revenir d'une migration
```

### Voir l'état actuel

```sh
alembic current
alembic history
```

---

## 9. Flux d'authentification & redirections

- À la connexion, le frontend appelle `POST /auth/login` et stocke le token JWT dans `localStorage`.
- Tous les appels API passent par `src/api/client.js` qui ajoute automatiquement :
  - `Authorization: Bearer <token>` si le token est présent.
- Le routeur Vue (`src/router/index.js`) protège les pages :
  - routes avec `meta.requiresAuth: true` → si **pas de token**, redirection vers `/login`
  - routes avec `meta.guestOnly: true` → si **token présent**, redirection vers `/`

---

## 10. Notes d'architecture

- `FastAPI_App/` : API Application (utilisateurs, auth, historique, favoris)
- `FastAPI_ML/` : API ML (données de matchs + modèle scikit-learn)
- `Data/` : documentation du schéma SQL (référence, non exécutable directement)
- `Data/seeds/` : scripts SQL de seeding idempotents
- Chaque API a son propre `venv`, `requirements.txt` et configuration Alembic
- Le fichier `.env` est **unique à la racine** et partagé entre les deux APIs
- Les migrations sont **versionnées dans Git** (dossier `alembic/versions/`)