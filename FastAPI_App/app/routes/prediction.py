from fastapi import APIRouter, Depends, HTTPException, status
import httpx
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.prediction import PredictionRequest, PredictionResponse
from ..schemas.user import PredictionHistoryOut
from ..routes.auth import get_current_user
from ..models.user import User, PredictionHistory
from ..core.config import settings

router = APIRouter(prefix="/predictions", tags=["Predictions"])

@router.get("/teams")
async def get_teams():
    async with httpx.AsyncClient() as client:
        try:
            ml_url = f"http://localhost:8001/teams"
            response = await client.get(ml_url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Erreur de communication avec le service ML: {str(e)}"
            )

from pydantic import BaseModel
from typing import Optional

class PredictionHistoryCreate(BaseModel):
    home_team_name: str
    home_team_logo_url: Optional[str] = None
    away_team_name: str
    away_team_logo_url: Optional[str] = None
    predicted_result: str
    confidence_score: float

@router.post("/history", response_model=PredictionHistoryOut)
def save_prediction_history(
    data: PredictionHistoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_prediction = PredictionHistory(
        user_id=current_user.id,
        home_team_name=data.home_team_name,
        home_team_logo_url=data.home_team_logo_url,
        away_team_name=data.away_team_name,
        away_team_logo_url=data.away_team_logo_url,
        predicted_result=data.predicted_result,
        confidence_score=data.confidence_score
    )
    db.add(new_prediction)
    db.commit()
    db.refresh(new_prediction)
    return new_prediction

@router.get("/history", response_model=List[PredictionHistoryOut])
def get_prediction_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Retourne l'historique filtré par utilisateur
    return db.query(PredictionHistory).filter(PredictionHistory.user_id == current_user.id).all()

def register_routes(app):
    app.include_router(router)
