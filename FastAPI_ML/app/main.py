from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.predict import register_routes
from .core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API ML (données de matchs, entraînement et prédiction) pour la Match Prediction App.",
    version=settings.PROJECT_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from .database import engine, Base, SessionLocal
from .models.match import Team

# Création des tables (pour le mode dev/démo sans PostgreSQL)
Base.metadata.create_all(bind=engine)

# Seeding des équipes si la table est vide
db = SessionLocal()
try:
    if db.query(Team).count() == 0:
        teams = [
            Team(id=1, name="Paris Saint-Germain"),
            Team(id=2, name="Monaco"),
            Team(id=3, name="Brest"),
            Team(id=4, name="Lille"),
            Team(id=5, name="Nice"),
            Team(id=6, name="Lyon"),
            Team(id=7, name="Lens"),
            Team(id=8, name="Marseille"),
            Team(id=9, name="Reims"),
            Team(id=10, name="Rennes"),
            Team(id=11, name="Toulouse"),
            Team(id=12, name="Montpellier"),
            Team(id=13, name="Strasbourg"),
            Team(id=14, name="Le Havre"),
            Team(id=15, name="Nantes"),
            Team(id=16, name="Angers"),
            Team(id=17, name="Saint-Étienne"),
            Team(id=18, name="Auxerre")
        ]
        db.add_all(teams)
        db.commit()
finally:
    db.close()

register_routes(app)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "ml-api"}

