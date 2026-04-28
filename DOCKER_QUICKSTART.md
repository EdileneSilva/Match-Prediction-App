# 🐳 Docker Quickstart — Match Prediction App

Guide rapide pour lancer le projet après un `git clone`.

---

## Prérequis

- [Docker](https://docs.docker.com/get-docker/) installé
- [Docker Compose](https://docs.docker.com/compose/install/) installé (inclus avec Docker Desktop)

---

## 1. Cloner le projet

```bash
git clone <url-du-repo>
cd Match-Prediction-App
```

## 2. Configurer les variables d'environnement

```bash
cp .env.example .env
```

> Le fichier `.env` par défaut fonctionne tel quel pour le développement local.  
> Pour la production, changez au minimum `SECRET_KEY`.

## 3. Lancer tous les services

```bash
docker compose up --build
```

Cela démarre les 4 conteneurs :

| Conteneur | Service | URL |
|-----------|---------|-----|
| `frontend_container` | Vue 3 Frontend | [http://localhost:8080](http://localhost:8080) |
| `fastapi_app_container` | API App | [http://localhost:8000/docs](http://localhost:8000/docs) |
| `fastapi_ml_container` | API ML | [http://localhost:8001/docs](http://localhost:8001/docs) |
| `postgres_db` | PostgreSQL | `localhost:5432` |

> La première fois, le build peut prendre quelques minutes.

## 4. Entraîner le modèle ML (première utilisation)

Le modèle n'est pas pré-entraîné. Après le démarrage, lancez l'entraînement :

```bash
# Importer les données CSV en base
curl -X POST http://localhost:8001/ingestion/import

# Entraîner le modèle
curl -X POST http://localhost:8001/train
```

Ou utilisez les Swagger UI :
- [http://localhost:8001/docs](http://localhost:8001/docs) → `POST /ingestion/import` puis `POST /train`

## 5. Utiliser l'application

Ouvrez [http://localhost:8080](http://localhost:8080) dans votre navigateur.

1. Créez un compte (`/register`)
2. Connectez-vous (`/login`)
3. Allez sur **Prédiction** → sélectionnez deux équipes → lancez la prédiction

---

## Commandes utiles

### Démarrer / Arrêter

```bash
# Démarrer en arrière-plan (détaché)
docker compose up -d --build

# Voir les logs
docker compose logs -f

# Voir les logs d'un seul service
docker compose logs -f api-app
docker compose logs -f api-ml
docker compose logs -f frontend
docker compose logs -f postgres

# Arrêter tous les conteneurs
docker compose down

# Arrêter et supprimer les volumes (⚠️ perte de données)
docker compose down -v
```

### Reconstruire un seul service

```bash
docker compose up -d --build api-app
docker compose up -d --build api-ml
docker compose up -d --build frontend
```

### Accéder à un conteneur

```bash
# Shell dans l'API App
docker compose exec api-app bash

# Shell dans l'API ML
docker compose exec api-ml bash

# Shell dans PostgreSQL
docker compose exec postgres psql -U postgres
```

### Base de données

```bash
# Lister les bases
docker compose exec postgres psql -U postgres -c "\l"

# Se connecter à footballapp_db
docker compose exec postgres psql -U postgres -d footballapp_db

# Se connecter à footballprediction_db
docker compose exec postgres psql -U postgres -d footballprediction_db

# Réinitialiser la BDD (supprime le volume)
docker compose down -v
docker compose up -d --build
```

### Santé des services

```bash
# Healthcheck API App
curl http://localhost:8000/health

# Healthcheck API ML
curl http://localhost:8001/health

# Statut des conteneurs
docker compose ps
```

---

## Dépannage

| Problème | Solution |
|----------|----------|
| Port 5432 déjà utilisé | Une autre instance PostgreSQL tourne en local. Arrêtez-la ou changez le port dans `docker-compose.yml` |
| Port 8000/8001 déjà utilisé | Changez les ports dans `docker-compose.yml` (ex: `"8001:8001"` → `"8011:8001"`) |
| `Service ML inaccessible` | Vérifiez que `api-ml` tourne : `docker compose ps` et `docker compose logs api-ml` |
| Modèle non trouvé | Lancez `POST /ingestion/import` puis `POST /train` sur l'API ML |
| Erreur de connexion BDD | Attendez que `postgres` soit healthy : `docker compose logs postgres` |

---

## Résumé rapide (copier-coller)

```bash
git clone <url-du-repo> && cd Match-Prediction-App
cp .env.example .env
docker compose up -d --build
# Attendre ~30s que tout démarre, puis :
curl -X POST http://localhost:8001/ingestion/import
curl -X POST http://localhost:8001/train
# Ouvrir http://localhost:8080
```
