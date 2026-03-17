from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import register_routes


app = FastAPI(
    title="Match Prediction App - Application API",
    description="API Application (utilisateurs, historique, favoris, prédictions) pour la Match Prediction App.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_routes(app)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "app-api"}

