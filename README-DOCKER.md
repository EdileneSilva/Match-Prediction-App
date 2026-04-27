# 🐋 README Docker pour Match Prediction App

Guide complet pour lancer l'application avec Docker. Conçu pour les nouveaux utilisateurs qui viennent de cloner le dépôt.

## ⚡ Démarrage Rapide

### Prérequis
- Docker Desktop installé
- Git cloné : `git clone <votre-repo-url>`

### Installation en 5 commandes

```bash
# 1. Cloner et se déplacer dans le projet
git clone <votre-repo-url>
cd Match-Prediction-App

# 2. Configurer les variables d'environnement
cp .env.example .env

# 3. Construire les images Docker
docker build -t postgres-db ./Data
docker build -t api-app ./FastAPI_App
docker build -t api-ml ./FastAPI_ML  
docker build -t frontend ./match_prediction_app-front

# 4. Démarrer les conteneurs
docker start postgres_db fastapi_api fastapi_ml frontend_app

# 5. Initialiser les bases de données (dans un nouveau terminal)
docker exec -it postgres psql -U postgres -f /docker-entrypoint-initdb.d/MCD.sql
docker exec -it postgres psql -U postgres -f /docker-entrypoint-initdb.d/MCD_app.sql
```

### Vérification
- **Frontend** : http://localhost:8080
- **API Application** : http://localhost:8000/docs
- **API ML** : http://localhost:8001/docs
- **Base de données** : localhost:5432

---

## 📋 Architecture Docker

L'application Dockerisée inclut 4 services :

| Service | Port | Description | Accès |
|---------|------|-------------|-------|
| **Frontend Vue.js** | 8080 | Interface utilisateur | http://localhost:8080 |
| **API Application** | 8000 | Auth, utilisateurs, historique | http://localhost:8000/docs |
| **API ML** | 8001 | Prédictions, modèle ML | http://localhost:8001/docs |
| **PostgreSQL** | 5432 | Bases de données | postgres:postgres@localhost:5432 |

---

## 🛠️ Commandes Docker Essentielles

### Démarrage et Arrêt
```bash
# Démarrer les conteneurs
docker start postgres_db api_app api_ml frontend_app

# Arrêter les conteneurs
docker stop postgres_db api_app api_ml frontend_app

# Redémarrer un conteneur spécifique
docker restart api_app

# Voir les conteneurs en cours
docker ps

# Voir tous les conteneurs (y compris arrêtés)
docker ps -a
```

### Nettoyage Complet
```bash
# Arrêter et supprimer les conteneurs
docker stop postgres_db api_app api_ml frontend_app
docker rm postgres_db api_app api_ml frontend_app

# Supprimer les images
docker rmi api_app api_ml frontend postgres_db

# Nettoyage complet Docker
docker system prune -f
docker volume prune -f
```

---

## 🔧 Configuration

### Fichier .env
Le `.env` à la racine contient toute la configuration :

```env
# Bases de données (configuré pour Docker)
DATABASE_APP_URL=postgresql://postgres:postgres@postgres:5432/footballapp_db
DATABASE_ML_URL=postgresql://postgres:postgres@postgres:5432/footballprediction_db

# Authentification JWT
SECRET_KEY=change-me-en-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# MLFlow
MLFLOW_TRACKING_URI=sqlite:///mlflow.db
```

### Points Importants
- En Docker, utilisez `postgres:5432` (nom du conteneur) au lieu de `localhost:5432`
- Les données persistent dans les volumes Docker
- Les ports sont mappés : 8000, 8001, 8080, 5432
- Utilisez `--link` pour connecter les conteneurs entre eux

---

## 🚀 Workflow de Développement

### Pour les Développeurs
1. **Modifier le code** : Les fichiers sont synchronisés en temps réel
2. **Reconstruire** : `docker build -t api-app ./FastAPI_App` après modifications importantes
3. **Redémarrer** : `docker restart api-app` pour appliquer les changements 
4. **Hot reload** : Les APIs et le frontend se rechargent automatiquement

### Base de Données
- Les données persistent même après `docker stop`
- Pour réinitialiser : `docker stop postgres && docker rm postgres && docker run -d --name postgres -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres postgres:15`

---

## 📁 Structure des Fichiers Docker

```
Match-Prediction-App/
├── .env                        # Configuration partagée
├── README-DOCKER.md           # Ce fichier
├── FastAPI_App/
│   ├── Dockerfile.api         # API Application
│   └── requirements.txt
├── FastAPI_ML/
│   ├── Dockerfile             # API ML
│   └── requirements.txt
├── match_prediction_app-front/
│   ├── Dockerfile             # Frontend Vue.js
│   └── package.json
└── Data/
    ├── MCD.sql                # Base ML
    └── MCD_app.sql            # Base Application
```

---
### Interfaces Web
- **Application frontend** : http://localhost:8080
- **Documentation API App** : http://localhost:8000/docs
- **Documentation API ML** : http://localhost:8001/docs

### Base de Données
```bash
# Se connecter à PostgreSQL
docker exec -it postgres_db psql -U postgres

# Lister les bases de données
\l
# Vous devriez voir : footballapp_db et footballprediction_db
```

---

## 💡 Conseils d'Utilisation

### Pour les Nouveaux Utilisateurs
1. **Lisez ce README en entier** avant de commencer
2. **Suivez les étapes dans l'ordre** : ne sautez pas l'initialisation de la BDD
3. **Utilisez les logs** pour diagnostiquer les problèmes
4. **Sauvegardez votre .env** avec vos clés secrètes

### Bonnes Pratiques
- **Ne partagez jamais** votre fichier `.env`
- **Utilisez des secrets forts** en production
- **Sauvegardez régulièrement** vos données de la base de données
- **Surveillez les logs** pour détecter les problèmes

---

🎉 **Si tout fonctionne, votre application est prête !**

Accédez à http://localhost:8080 pour commencer à utiliser l'application de prédiction de matchs.
