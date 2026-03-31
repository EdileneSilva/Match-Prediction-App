from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes.base import register_routes

from .core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API Application (utilisateurs, historique, favoris, prédictions) pour la Match Prediction App.",
    version=settings.PROJECT_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080", "http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from .database import engine, Base, SessionLocal
from .models.user import User

# Création des tables (pour le mode dev/démo sans PostgreSQL)
Base.metadata.create_all(bind=engine)

# Initialisation d'un utilisateur par défaut pour l'historique
db = SessionLocal()
try:
    if not db.query(User).filter(User.id == 1).first():
        default_user = User(
            id=1,
            username="dev_user",
            email="dev@example.com",
            hashed_password="fake_hashed_password"
        )
        db.add(default_user)
        db.commit()
finally:
    db.close()

register_routes(app)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "app-api"}

