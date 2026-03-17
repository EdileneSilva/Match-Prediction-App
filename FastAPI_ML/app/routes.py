from fastapi import APIRouter, FastAPI

from .services.ml_service import predict_match as ml_predict_match
from .schemas.team import TeamCreate, Team
from .schemas.match import MatchCreate, Match


router = APIRouter()


@router.get("/", tags=["Root"])
def root():
    return {"message": "Match Prediction App - ML API"}


@router.post("/predict", tags=["Prediction"])
def predict():
    # Stub de prédiction : renvoie un résultat fixe
    result = ml_predict_match({})
    return result


def register_routes(app: FastAPI) -> None:
    app.include_router(router)

