# 🐋 Docker Compose - Match Prediction App

Instructions pour lancer l'application complète avec Docker Compose.

## 🚀 Démarrage Rapide

### 1. Prérequis
- Docker Desktop installé
- Docker Compose disponible

### 2. Configuration de l'environnement
```bash
# Copier le fichier d'environnement
cp .env.docker .env
```

### 3. Lancer tous les services
```bash
# Construire et démarrer tous les conteneurs
docker-compose up --build

# Ou en mode détaché (background)
docker-compose up --build -d
```

### 4. Vérifier que tout fonctionne
- **Frontend Vue.js** : http://localhost:8080
- **API Application** : http://localhost:8000/docs
- **API ML** : http://localhost:8001/docs
- **Base de données** : postgres:postgres@localhost:5432

## 📋 Services Configurés

| Service | Port | Description | Conteneur |
|---------|------|-------------|-----------|
| **Frontend** | 8080 | Interface utilisateur Vue.js | frontend_container |
| **API App** | 8000 | Auth, utilisateurs, favoris | fastapi_app_container |
| **API ML** | 8001 | Prédictions, modèle ML | fastapi_ml_container |
| **PostgreSQL** | 5432 | Bases de données | postgres_db |

## 🛠️ Commandes Utiles

### Gestion des conteneurs
```bash
# Démarrer les services
docker-compose up -d

# Arrêter les services
docker-compose down

# Reconstruire après modifications
docker-compose up --build

# Voir les logs
docker-compose logs -f

# Logs d'un service spécifique
docker-compose logs -f api-app
```

### Développement
```bash
# Redémarrer un service spécifique
docker-compose restart api-app

# Entrer dans un conteneur
docker-compose exec api-app bash

# Voir l'état des services
docker-compose ps
```

### Nettoyage
```bash
# Arrêter et supprimer les conteneurs
docker-compose down

# Supprimer les volumes (attention: perte de données)
docker-compose down -v

# Nettoyage complet
docker-compose down -v --rmi all
```

## 🔧 Configuration

### Variables d'environnement
Le fichier `.env` contient toute la configuration :
- Bases de données PostgreSQL
- Clés JWT pour l'authentification
- Configuration MLFlow
- URLs des APIs pour le frontend

### Volumes persistants
- `postgres_data` : Données PostgreSQL persistantes
- Volumes de montage pour le développement (hot reload)

## 🐛 Dépannage

### Problèmes courants
1. **Port déjà utilisé** : Vérifiez qu'aucun autre service n'utilise les ports 5432, 8000, 8001, 8080
2. **Base de données inaccessible** : Attendez que PostgreSQL soit complètement démarré
3. **Build échoue** : Vérifiez que tous les Dockerfiles sont présents

### Vérifier l'état
```bash
# État des services
docker-compose ps

# Santé de la base de données
docker-compose exec postgres pg_isready -U postgres

# Tester les APIs
curl http://localhost:8000/docs
curl http://localhost:8001/docs
```

## 📁 Structure des fichiers

```
Match-Prediction-App/
├── docker-compose.yml          # Configuration principale
├── .env.docker                 # Variables d'environnement
├── docker-compose-instructions.md # Ce fichier
├── FastAPI_App/
│   ├── Dockerfile.api
│   └── requirements.txt
├── FastAPI_ML/
│   ├── Dockerfile
│   └── requirements.txt
├── match_prediction_app-front/
│   ├── Dockerfile
│   └── package.json
└── Data/
    ├── MCD.sql
    └── MCD_app.sql
```

🎉 **Votre application est maintenant prête avec Docker Compose !**
