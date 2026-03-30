from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.predict import register_routes
from .routes.data import router as data_router
from .routes.train import register_routes as register_train_routes
from .core.config import settings
from .database import engine, Base
from .models.match import Team, FootballMatch, MatchStats, TeamStatsReference, TrainLog

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


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


register_routes(app)
app.include_router(data_router)
register_train_routes(app)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "ml-api"}