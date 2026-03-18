from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.match import PredictionRequest, PredictionResponse
from ..schemas.team import Team as TeamSchema
from ..services.ml_service import ml_service
from ..models.match import Team

router = APIRouter(tags=["ML Prediction"])

@router.get("/teams", response_model=List[TeamSchema])
def get_teams(db: Session = Depends(get_db)):
    return db.query(Team).all()

@router.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest, db: Session = Depends(get_db)):
    # Vérification que les équipes existent
    home_team = db.query(Team).filter(Team.id == request.home_team_id).first()
    away_team = db.query(Team).filter(Team.id == request.away_team_id).first()
    
    if not home_team or not away_team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="L'une ou les deux équipes sont introuvables."
        )
    
    prediction = ml_service.predict_match(request.home_team_id, request.away_team_id)
    
    return {
        "home_team_id": request.home_team_id,
        "away_team_id": request.away_team_id,
        **prediction
    }

def register_routes(app):
    app.include_router(router)
