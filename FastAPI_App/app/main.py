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

register_routes(app)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "app-api"}

