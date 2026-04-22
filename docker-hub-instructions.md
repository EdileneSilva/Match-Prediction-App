# Instructions Docker Hub pour Match Prediction App

## 1. Construction et Push des images sur Docker Hub

### Prérequis
- Avoir un compte Docker Hub
- Être connecté : `docker login`

### Construction des images
```bash
# Image API FastAPI
cd FastAPI_App
docker build -f Dockerfile.api -t votre-username/match-prediction-api:latest .
docker push votre-username/match-prediction-api:latest

# Image ML FastAPI
cd ../FastAPI_ML
docker build -t votre-username/match-prediction-ml:latest .
docker push votre-username/match-prediction-ml:latest

# Image Frontend
cd ../match_prediction_app-front
docker build -t votre-username/match-prediction-frontend:latest .
docker push votre-username/match-prediction-frontend:latest
```

## 2. docker-compose.yml pour production (avec images Docker Hub)

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    container_name: postgres_db
    environment:
      POSTGRES_DB: footballprediction_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./Data/MCD.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    networks:
      - app-network
    restart: unless-stopped

  fastapi:
    image: votre-username/match-prediction-api:latest
    container_name: fastapi_api
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/footballprediction_db
      DATABASE_APP_URL: postgresql://postgres:postgres@postgres:5432/footballprediction_db
      DATABASE_ML_URL: postgresql://postgres:postgres@postgres:5432/footballprediction_db
      ML_API_URL: http://fastapi-ml:8001
      SECRET_KEY: change-me-in-production
      ALGORITHM: HS256
      ACCESS_TOKEN_EXPIRE_MINUTES: 60
    ports:
      - "8000:8000"
    volumes:
      - ./Data:/app/Data
    depends_on:
      - postgres
    networks:
      - app-network
    restart: unless-stopped

  fastapi-ml:
    image: votre-username/match-prediction-ml:latest
    container_name: fastapi_ml
    environment:
      DATABASE_ML_URL: postgresql://postgres:postgres@postgres:5432/footballprediction_db
      MODEL_PATH: /app/Data/dataset/match_model_v1.joblib
      DATASET_PATH: /app/Data/dataset/completed_match_dataset_final.csv
      DATA_DIR: /app/Data
    ports:
      - "8001:8001"
    volumes:
      - ./Data:/app/Data
    depends_on:
      - postgres
    networks:
      - app-network
    restart: unless-stopped

  frontend:
    image: votre-username/match-prediction-frontend:latest
    container_name: frontend_app
    ports:
      - "80:80"
    depends_on:
      - fastapi
      - fastapi-ml
    networks:
      - app-network
    restart: unless-stopped

volumes:
  postgres_data:
    driver: local

networks:
  app-network:
    driver: bridge
```

## 3. Lancement avec Docker Compose

```bash
# Lancer tous les services
docker-compose up -d

# Vérifier les services
docker-compose ps

# Voir les logs
docker-compose logs -f

# Arrêter les services
docker-compose down
```

## 4. Accès à l'application

- Frontend : http://localhost:80
- API FastAPI : http://localhost:8000
- API ML : http://localhost:8001
- Documentation API : http://localhost:8000/docs
- Base de données : localhost:5432
