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

register_routes(app)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "ml-api"}

