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
    return db.query(Team).all()

@router.post("/predict")
def predict(request: MatchRequest):
    """
    **Générer une Prédiction ML**
    
    Évalue l'issue probable du match en s'appuyant sur notre modèle Stacking
    (combinant RandomForest, XGBoost, et Régression Logistique).
    
    - **home_team** : Nom de l'équipe à domicile.
    - **away_team** : Nom de l'équipe à l'extérieur.
    - **referee** : Nom de l'arbitre principal.
    - **season** : Année de début de la saison (ex: 2024).
    - **round** : Numéro de la journée du championnat.
    
    Retourne la `prediction`, la `confidence` globale, et les probabilités par issue.
    """
    prediction_result = ml_service.predict_match(
        request.home_team, 
        request.away_team,
        request.referee,
        request.season,
        request.round,
    )
    
    return prediction_result

def register_routes(app):
    app.include_router(router)
