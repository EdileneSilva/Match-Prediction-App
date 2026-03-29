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

@router.post("/predict", response_model=PredictionResponse)
async def predict_match(
    request: PredictionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 1. Appel à l'API ML
    # Note: On suppose ici que le frontend envoie les IDs des équipes (que l'on récupérera via GET /teams de ML API via APP API proxy ou direct)
    # Pour l'instant, simplifions : on cherche les IDs via FastAPI_ML/teams si besoin, 
    # ou le frontend les a déjà. Admettons que le frontend envoie des IDs.
    # On va modifier le schéma PredictionRequest pour accepter les IDs.
    
    async with httpx.AsyncClient() as client:
        try:
            # On simule l'appel à l'API ML
            # ML_API_URL devrait être dans settings
            ml_url = f"http://localhost:8001/predict" 
            
            ml_request = {
                "home_team": request.home_team_name,
                "away_team": request.away_team_name,
                "referee": "Unknown",  # Valeur par défaut
                "season": 2024,        # Valeur par défaut
                "round": 1             # Valeur par défaut
            }
            
            response = await client.post(ml_url, json=ml_request)
            response.raise_for_status()
            ml_data = response.json()
            
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Erreur de communication avec le service ML: {str(e)}"
            )

    # 2. Enregistrement dans l'historique
    new_prediction = PredictionHistory(
        user_id=current_user.id,
        home_team_name=request.home_team_name,
        home_team_logo_url=request.home_team_logo_url,
        away_team_name=request.away_team_name,
        away_team_logo_url=request.away_team_logo_url,
        predicted_result=ml_data["prediction"],
        confidence_score=ml_data["confidence"]
    )
    db.add(new_prediction)
    db.commit()
    db.refresh(new_prediction)

    return {
        "predicted_result": ml_data["prediction"],
        "confidence_score": ml_data["confidence"]
    }

@router.get("/history", response_model=List[PredictionHistoryOut])
def get_prediction_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Retourne l'historique filtré par utilisateur
    return db.query(PredictionHistory).filter(PredictionHistory.user_id == current_user.id).all()

def register_routes(app):
    app.include_router(router)
