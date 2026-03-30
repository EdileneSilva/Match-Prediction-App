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
def predict(request: MatchRequest, db: Session = Depends(get_db)):
    
    # Vérification que les équipes existent
    # home_team = db.query(Team).filter(Team.id == request.home_team_id).first()
    # away_team = db.query(Team).filter(Team.id == request.away_team_id).first()
    
    # if not home_team or not away_team:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="L'une ou les deux équipes sont introuvables."
    #     )
    
    prediction = ml_service.predict_match(
        request.home_team, 
        request.away_team,
        request.referee,
        request.season,
        request.league_round,
    )
    
    return {
        "home_team": request.home_team,
        "away_team": request.away_team,
        "season": request.season,
        "league_round": request.league_round,
        **prediction
    }

def register_routes(app):
    app.include_router(router)
