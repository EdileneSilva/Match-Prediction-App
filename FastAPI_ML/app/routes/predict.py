from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..schemas.request import MatchRequest
from ..database import get_db
from ..schemas.team import Team as TeamSchema
from ..services.ml_service import ml_service
from ..models.match import Team

router = APIRouter(tags=["ML Prediction"])


@router.get("/teams", response_model=List[TeamSchema])
def get_teams(db: Session = Depends(get_db)):
    """Retourne la liste de toutes les équipes disponibles."""
    return db.query(Team).all()


@router.post("/predict")
def predict(request: MatchRequest, db: Session = Depends(get_db)):
    """
    Prédit le résultat d'un match entre deux équipes.

    Les noms des équipes sont validés en base avant d'appeler le modèle ML.
    Les statistiques sont lues depuis team_stats_reference (Feature Store).
    """
    # Validation des équipes en base
    home_team = db.query(Team).filter(Team.name == request.home_team).first()
    away_team = db.query(Team).filter(Team.name == request.away_team).first()

    if not home_team or not away_team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="L'une ou les deux équipes sont introuvables."
        )

    # Vérification que le modèle est chargé
    if not ml_service.is_model_loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Modèle ML non chargé. Lancez POST /train d'abord."
        )

    # Vérification que les stats sont disponibles
    if ml_service.home_stats is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Statistiques de référence non disponibles. Lancez POST /train d'abord."
        )

    try:
        result = ml_service.predict_match(
            home_team = home_team.name,
            away_team = away_team.name,
            season    = request.season,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la prédiction : {e}"
        )

    return {
        "home_team": home_team.name,
        "away_team": away_team.name,
        "season":    request.season,
        **result,
    }


def register_routes(app):
    app.include_router(router)