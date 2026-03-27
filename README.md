![Match Prediction App](docs/match-prediction-banner.jpg)

# 🏆 Match Prediction App - MVP

Cette application est un MVP (Minimum Viable Product) entrepreneurial permettant de prédire l'issue de matchs de Ligue 1 (Victoire Domicile, Nul, Victoire Extérieure) grâce à un modèle d'Intelligence Artificielle de classification.

Ce projet a été conçu en 5 semaines avec une approche Agile et Lean Startup.

---

## 🏗️ Architecture du Projet

Le projet est composé de 3 microservices distincts pour une architecture moderne et scalable :

1.  **FastAPI_App (Backend Principal)** : Gère l'authentification (JWT), l'historique utilisateur, les favoris, et sert de proxy (traduction des IDs d'équipes en noms) vers l'API ML.
2.  **FastAPI_ML (Intelligence Engine)** : API d'inférence dédiée chargée d'exécuter le modèle de classification de stacking (Random Forest, XGBoost, Regression Logistique) et de renvoyer les probabilités.
3.  **Frontend (Vue.js 3)** : Interface utilisateur fluide permettant la création de compte, la consultation de l'historique et la soumission de nouvelles prédictions.

Chaque API possède sa propre base de données (**PostgreSQL** en production, **SQLite** en développement rapide).

---

## ⚡ Guide d'Installation Rapide (< 15 min)

### Pré-requis
- **Python 3.12+**
- **Node.js 18+** et **npm**
- Optionnel : PostgreSQL si vous souhaitez utiliser l'environnement de production. *Par défaut, l'application utilise SQLite in-memory pour un démarrage immédiat en local.*

Ouvrez **3 terminaux séparés** à la racine du projet.

### Terminal 1 : Backend Principal (FastAPI_App)
```bash
cd FastAPI_App
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
pip install -r requirements.txt

# Lancement du serveur sur le port 8000
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
*La base de données SQLite `app.db` se créera automatiquement.*

### Terminal 2 : Moteur d'Intelligence Artificielle (FastAPI_ML)
```bash
cd FastAPI_ML
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
pip install -r requirements.txt

# Lancement du serveur sur le port 8001
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```
*La base de données SQLite `ml_app.db` se créera et se peuplera automatiquement avec les équipes.*

### Terminal 3 : Frontend (Vue.js)
```bash
cd match_prediction_app-front
npm install
npm run serve
```
*L'application UI est désormais accessible sur **http://localhost:8080** !*

---

## 📚 Documentation API (Swagger / OpenAPI)

Les deux APIs sont auto-documentées avec FastAPI, intégrant le standard OpenAPI. Une fois les serveurs lancés, accédez aux Swagger UIs :

- 🔐 **FastAPI_App (Users, Historique, Proxy)** : [http://localhost:8000/docs](http://localhost:8000/docs)
- 🧠 **FastAPI_ML (Modèle de Prédiction)** : [http://localhost:8001/docs](http://localhost:8001/docs)

---

## 🧪 Tests Automatisés

Le projet inclut une couverture de test complète via `pytest` (tests unitaires, d'intégration, et parcours E2E complet).

```bash
# Pour tester FastAPI_App (34 tests)
cd FastAPI_App
export PYTHONPATH=$PYTHONPATH:.
pytest tests/ -v

# Pour tester FastAPI_ML (3 tests)
cd FastAPI_ML
export PYTHONPATH=$PYTHONPATH:.
pytest tests/ -v
```

---

## 📊 Modèle Machine Learning & Données

- **Classification Supervisée** : Le modèle prédit un résultat 1N2 (HOME_WIN, DRAW, AWAY_WIN).
- **Architecture Modèle** : Ensemble de Stacking (Random Forest, XGBoost, LR) pour maximiser la résilience aux variations imprévisibles du football (Calibration active des probabilités).
- **Sources de données** : API Football pour les statistiques et cotes, complétées par du web scraping et datasets CSV statiques pour les données d'historiques.

---

## ⚙️ Configuration Avancée (PostgreSQL)

Pour utiliser PostgreSQL en production à la place de SQLite, configurez vos fichiers `.env` dans chaque dossier d'API.

Dans `FastAPI_App/.env` :
```env
DATABASE_APP_URL=postgresql://root:password@localhost:5432/footballapp_db
```

Dans `FastAPI_ML/.env` :
```env
DATABASE_ML_URL=postgresql://root:password@localhost:5432/footballml_db
```

*Des scripts d'initialisation MCD sont disponibles dans le dossier `Data/`.*

---

*Projet développé dans le cadre d'un MVP Entrepreneurial.*