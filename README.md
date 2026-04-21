![Match Prediction App](docs/match-prediction-banner.jpg)

# Match Prediction App

Application complète de prédiction de matchs de Ligue 1 avec :
- 2 APIs FastAPI séparées (Application & ML)
- 2 bases PostgreSQL séparées (utilisateurs/historique & données de matchs)
- 1 frontend Vue.js 3

Ce README explique comment installer et lancer le projet pour une première utilisation ou sur une nouvelle machine.

---

## 1. Pré‑requis

- **Python 3.12+**
- **Node.js 18+** et npm
- **PostgreSQL** (local) avec accès superuser `postgres`

---

## 2. Bases de données PostgreSQL

L'application utilise deux bases de données distinctes. Créez-les à partir des scripts SQL fournis :

```sh
# Crée la base footballprediction_db (Données ML)
psql -U postgres -f Data/MCD.sql

# Crée la base footballapp_db (Utilisateurs & Historique)
psql -U postgres -f Data/MCD_app.sql
```

---

## 3. Configuration de l'environnement (.env)

Le projet utilise un **fichier `.env` unique à la racine** pour simplifier la gestion. Les deux backends sont configurés pour lire ce fichier automatiquement.

1. Copiez le fichier d'exemple :
   ```sh
   cp .env.example .env
   ```
2. Adaptez le contenu de `.env` si nécessaire (notamment les identifiants PostgreSQL).

**Contenu de base attendu :**
```env
DATABASE_APP_URL=postgresql://postgres:postgres@localhost:5432/footballapp_db
DATABASE_ML_URL=postgresql://postgres:postgres@localhost:5432/footballprediction_db

ML_API_URL=http://localhost:8001
SECRET_KEY=votre-cle-secrete-tres-longue
```

---

## 4. Lancement des Backends (FastAPI)

Vous devez lancer les deux APIs dans des terminaux séparés.

### 4.1. API Application (`FastAPI_App`)
Gère l'auth, les favoris et l'historique.

```sh
cd FastAPI_App
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Vérification : `curl http://localhost:8000/health`

### 4.2. API ML (`FastAPI_ML`)
Gère les données de matchs et les prédictions.

```sh
cd FastAPI_ML
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```
Vérification : `curl http://localhost:8001/health`

---

## 5. Lancement du Frontend (Vue.js)

```sh
cd match_prediction_app-front
npm install
npm run serve
```
L'application sera accessible sur `http://localhost:8080`.

---

## 6. Structure du projet

- `Data/` : Scripts SQL et datasets (CSV/Joblib).
- `FastAPI_App/` : Logique utilisateur, authentification JWT, historique.
- `FastAPI_ML/` : Modèle de prédiction, statistiques de matchs.
- `match_prediction_app-front/` : Interface utilisateur Vue 3.
- `shared/` : Configuration et utilitaires partagés par les deux backends.

---

## 7. Notes importantes

- **Compte de test** : Au premier lancement, un utilisateur `dev_user` (email: `dev@example.com`) est automatiquement créé pour faciliter les tests locaux.
- **CORS** : Les APIs sont configurées pour accepter les requêtes provenant de `localhost:8080`.
- **Modèle ML** : Assurez-vous que le fichier `.joblib` est bien présent dans `Data/dataset/` pour que les prédictions fonctionnent.