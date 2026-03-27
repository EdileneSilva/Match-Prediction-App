from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from .routes.base import register_routes


from .core.config import settings

tags_metadata = [
    {
        "name": "Auth & Users",
        "description": "Opérations d'authentification (login, register) et gestion de profil utilisateur.",
    },
    {
        "name": "Predictions",
        "description": "Proxy vers le modèle ML pour effectuer des prédictions et consulter l'historique.",
    },
    {
        "name": "Health",
        "description": "Vérification de l'état de l'API.",
    },
]

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""
API principale de la **Match Prediction App**.

Cette API agit comme backend front-facing :
* Gère les utilisateurs et l'authentification sécurisée via JWT.
* Sauvegarde l'historique et les favoris.
* Sert de proxy vers l'API ML pour lancer les prédictions en traduisant les identifiants d'équipes en noms réels.
    """,
    version=settings.PROJECT_VERSION,
    openapi_tags=tags_metadata,
    contact={
        "name": "Équipe Produit",
        "email": "contact@matchprediction.com",
    }
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:5173",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montage du dossier statique pour les logos
static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static")
os.makedirs(static_path, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_path), name="static")

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

