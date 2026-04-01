from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes.base import register_routes
from .core.config import settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Toutes les opérations de démarrage DB sont ici.
    Utiliser lifespan évite les crashs au niveau module et les problèmes de hot-reload.
    """
    from .database import SessionLocal
    from .models.user import User

    db = SessionLocal()
    try:
        # 1. Utilisateur par défaut (dev)
        if not db.query(User).filter(User.id == 1).first():
            default_user = User(
                id=1,
                username="dev_user",
                email="dev@example.com",
                hashed_password="fake_hashed_password",
            )
            db.add(default_user)
            db.commit()
            print("✅ Utilisateur dev créé.")

    except Exception as e:
        db.rollback()
        print(f"⚠️  Erreur au démarrage (DB seed) : {e}")
    finally:
        db.close()

    yield  # L'application tourne ici


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API Application (utilisateurs, historique, favoris, prédictions) pour la Match Prediction App.",
    version=settings.PROJECT_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1|192\.168\.\d+\.\d+)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_routes(app)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "app-api"}
