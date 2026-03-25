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
            Team(id=1, name="Arsenal"),
            Team(id=2, name="Aston Villa"),
            Team(id=3, name="Bournemouth"),
            Team(id=4, name="Brentford"),
            Team(id=5, name="Brighton"),
            Team(id=6, name="Chelsea"),
            Team(id=7, name="Crystal Palace"),
            Team(id=8, name="Everton"),
            Team(id=9, name="Fulham"),
            Team(id=10, name="Liverpool"),
            Team(id=11, name="Man City"),
            Team(id=12, name="Man United"),
            Team(id=13, name="Newcastle"),
            Team(id=14, name="Nottingham Forest"),
            Team(id=15, name="Sheffield United"),
            Team(id=16, name="Tottenham"),
            Team(id=17, name="West Ham"),
            Team(id=18, name="Wolves"),
            Team(id=19, name="Luton"),
            Team(id=20, name="Burnley")
        ]
        db.add_all(teams)
        db.commit()
finally:
    db.close()

register_routes(app)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "ml-api"}

