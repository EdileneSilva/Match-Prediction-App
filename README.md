![Match Prediction App](docs/match-prediction-banner.jpg)

# Match Prediction App


Application complète de prédiction de matchs de Ligue 1 avec :
- 2 APIs FastAPI séparées (Application & ML)
- 2 bases PostgreSQL séparées (users/historique & données de matchs)
- 1 frontend Vue.js 3

Ce README explique comment installer et lancer **les deux backends** et **le frontend** pour que toute l’équipe puisse travailler sans galérer.

---

## 1. Pré‑requis

- Python 3.12+
- Node.js 18+ et npm
- PostgreSQL (local) avec accès superuser `postgres` ou équivalent

---

## 2. Bases de données PostgreSQL

Créer les deux bases à partir des scripts SQL du dossier `Data/` :

```sh
psql -U postgres -f Data/MCD.sql        # crée la base footballprediction_db (ML)
psql -U postgres -f Data/MCD_app.sql    # crée la base footballapp_db (Application)
```

Adapte l’utilisateur/mot de passe si besoin dans les URLs ci‑dessous.

---

## 3. API Application – `FastAPI_App`

Cette API gère :
- l’authentification JWT (`/auth/register`, `/auth/login`, `/auth/me`, etc.),
- les utilisateurs, les favoris, l’historique,
- les appels à l’API ML (plus tard).

### 3.1. Configuration

Dans la racine du projet (ex: `Match-Prediction-App/.env`), créer un fichier `.env` :

```sh
cp .env.example .env
```

Contenu minimal (à adapter) :

```env
DATABASE_APP_URL=postgresql://postgres:postgres@localhost:5432/footballapp_db
DATABASE_ML_URL=postgresql://postgres:postgres@localhost:5432/footballprediction_db
SECRET_KEY=change-me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

> Remarque : ce fichier `.env` est unique et se crée à la racine du projet.

### 3.2. Environnement virtuel & dépendances

```sh
cd FastAPI_App
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3.3. Lancement de l’API Application

```sh
cd FastAPI_App
source venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Vérification :

```sh
curl http://127.0.0.1:8000/health
# -> {"status":"ok","service":"app-api"}
```

---

## 4. API ML – `FastAPI_ML`

Cette API gère :
- la base `footballprediction_db` (équipes, matchs, stats),
- le modèle de classification (scikit‑learn),
- les endpoints `/train`, `/predict`, `/metrics` (en cours de construction, stub existant).

### 4.1. Configuration

Dans `Match-Prediction-App/`, le `.env` unique à la racine contient aussi la config de l’API ML :

```env
DATABASE_ML_URL=postgresql://postgres:postgres@localhost:5432/footballprediction_db
```

> Remarque : ce fichier `.env` est unique et se crée à la racine du projet.

### 4.2. Environnement virtuel & dépendances

```sh
cd FastAPI_ML
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4.3. Lancement de l’API ML

```sh
cd FastAPI_ML
source venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

Vérification :

```sh
curl http://127.0.0.1:8001/health
# -> {"status":"ok","service":"ml-api"}
```

---

## 5. Frontend Vue.js – `match_prediction_app-front`

Ce projet Vue 3 consomme l’API Application (`http://localhost:8000`) via `src/api/client.js`.

### 5.1. Installation des dépendances

```sh
cd match_prediction_app-front
npm install
```

### 5.2. Lancement du serveur de dev

```sh
cd match_prediction_app-front
npm run serve
```

Ouvre ensuite l’URL affichée (généralement `http://localhost:8080`).

---

## 6. Flux d’authentification & redirections

- À la connexion, le frontend appelle `POST /auth/login` et stocke le token JWT dans `localStorage`.
- Tous les appels API passent par `src/api/client.js` qui ajoute automatiquement le header :
  - `Authorization: Bearer <token>` si le token est présent.
- Le routeur Vue (`src/router/index.js`) protège les pages :
  - routes avec `meta.requiresAuth: true` → si **pas de token**, redirection automatique vers `/login`,
  - routes avec `meta.guestOnly: true` → si **token présent**, redirection vers `/`.

Conséquence :  
> Si un utilisateur ouvre l’application sans compte ni token, il arrive **toujours** sur la page de connexion.

---

## 7. Notes d’architecture (résumé du logbook)

- Le dossier historique `FastAPI/` (monolithique) a été supprimé.
- L’architecture est maintenant :
  - `FastAPI_App/` : API Application (utilisateurs, auth, historique, favoris).
  - `FastAPI_ML/` : API ML (données de matchs + modèle).
  - `Data/` : scripts SQL des 2 BDD (`MCD.sql`, `MCD_app.sql`).
  - `match_prediction_app-front/` : frontend Vue 3.
- Chaque API a :
  - son propre `requirements.txt`,
  - son propre `venv`,
  - mais une configuration `.env` unique à la racine du projet.

---