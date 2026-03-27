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

@router.post("/predict", response_model=PredictionResponse)
async def predict_match(
    request: PredictionRequest,
    # ⬇️ AUTH DÉSACTIVÉE TEMPORAIREMENT — REMETTRE EN PRODUCTION
    # current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère les noms des équipes par ID, puis appelle l'API ML pour la prédiction.
    """
    # 1. Mapping IDs -> Noms
    from ..models.team import Team
    home_team = db.query(Team).filter(Team.id == request.home_team_id).first()
    away_team = db.query(Team).filter(Team.id == request.away_team_id).first()

    if not home_team or not away_team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="L'une ou les deux équipes sont introuvables dans la base de données."
        )

    # 2. Appel à l'API ML
    async with httpx.AsyncClient() as client:
        try:
            # On utilise le nom complet pour l'API ML
            ml_url = f"http://localhost:8001/predict" 
            
            ml_request = {
                "home_team": home_team.name,
                "away_team": away_team.name,
                "referee": request.referee,
                "season": request.season,
                "round": request.round
            }
            
            response = await client.post(ml_url, json=ml_request)
            response.raise_for_status()
            ml_data = response.json()
            
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Erreur de communication avec le service ML: {str(e)}"
            )

    # 3. Enregistrement dans l'historique (user_id=1 en mode dev sans auth)
    # On utilise prediction et confidence (nouveaux noms)
    new_prediction = PredictionHistory(
        user_id=1,
        home_team_name=home_team.name,
        away_team_name=away_team.name,
        prediction=ml_data.get("prediction"),
        confidence=ml_data.get("confidence")
    )
    db.add(new_prediction)
    db.commit()
    db.refresh(new_prediction)

    return {
        "prediction": ml_data.get("prediction"),
        "confidence": ml_data.get("confidence")
    }

@router.get("/history", response_model=List[PredictionHistoryOut])
def get_prediction_history(
    # ⬇️ AUTH DÉSACTIVÉE TEMPORAIREMENT — REMETTRE EN PRODUCTION
    # current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(PredictionHistory).all()

def register_routes(app):
    app.include_router(router)
