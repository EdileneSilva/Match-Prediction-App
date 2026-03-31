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
    if db.query(Team).count() != 18:
        # On nettoie si le compte n'est plus bon (pour forcer le re-seed 2025/2026)
        db.query(Team).delete()
        teams = [
            Team(name="Angers SCO", logo_url="https://media.api-sports.io/football/teams/77.png"),
            Team(name="AJ Auxerre", logo_url="https://media.api-sports.io/football/teams/108.png"),
            Team(name="Stade Brestois 29", logo_url="https://media.api-sports.io/football/teams/106.png"),
            Team(name="Le Havre AC", logo_url="https://media.api-sports.io/football/teams/111.png"),
            Team(name="RC Lens", logo_url="https://media.api-sports.io/football/teams/116.png"),
            Team(name="LOSC Lille", logo_url="https://media.api-sports.io/football/teams/79.png"),
            Team(name="FC Lorient", logo_url="https://media.api-sports.io/football/teams/97.png"),
            Team(name="Olympique Lyonnais", logo_url="https://media.api-sports.io/football/teams/80.png"),
            Team(name="Olympique de Marseille", logo_url="https://media.api-sports.io/football/teams/81.png"),
            Team(name="FC Metz", logo_url="https://media.api-sports.io/football/teams/112.png"),
            Team(name="AS Monaco", logo_url="https://media.api-sports.io/football/teams/91.png"),
            Team(name="FC Nantes", logo_url="https://media.api-sports.io/football/teams/83.png"),
            Team(name="OGC Nice", logo_url="https://media.api-sports.io/football/teams/84.png"),
            Team(name="Paris FC", logo_url="https://media.api-sports.io/football/teams/269.png"),
            Team(name="Paris Saint-Germain", logo_url="https://media.api-sports.io/football/teams/85.png"),
            Team(name="Stade Rennais FC", logo_url="https://media.api-sports.io/football/teams/94.png"),
            Team(name="RC Strasbourg Alsace", logo_url="https://media.api-sports.io/football/teams/95.png"),
            Team(name="Toulouse FC", logo_url="https://media.api-sports.io/football/teams/96.png")
        ]
        db.add_all(teams)
        db.commit()
finally:
    db.close()

register_routes(app)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "ml-api"}

