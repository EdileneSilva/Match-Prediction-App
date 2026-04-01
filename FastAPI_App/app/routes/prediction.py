from fastapi import APIRouter, Depends, HTTPException, status
import httpx
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from ..database import get_db
from ..schemas.prediction import PredictionRequest, PredictionResponse
from ..schemas.user import PredictionHistoryOut
from ..routes.auth import get_current_user
from ..models.user import User, PredictionHistory
from ..models.team import Team
from ..core.config import settings

router = APIRouter(prefix="/predictions", tags=["Predictions"])


# ─────────────────────────────────────────────
# GET /predictions/teams
# Liste les équipes disponibles (depuis la BDD App)
# ─────────────────────────────────────────────
@router.get("/teams")
def get_teams(db: Session = Depends(get_db)):
    teams = db.query(Team).order_by(Team.name).all()
    return [{"id": team.id, "name": team.name, "logo_url": team.logo_url} for team in teams]


# ─────────────────────────────────────────────
# POST /predictions/predict
# Proxy vers l'API ML (port 8001) + sauvegarde historique
# ─────────────────────────────────────────────
class PredictRequest(BaseModel):
    home_team: str
    away_team: str
    season: Optional[str] = "2024/2025"


@router.post("/predict")
async def predict_match(
    data: PredictRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Proxy la requête vers l'API ML et sauvegarde le résultat dans l'historique.
    """
    # 1. Résolution des équipes en BDD (pour obtenir id et logo)
    home_team = db.query(Team).filter(Team.name == data.home_team).first()
    away_team = db.query(Team).filter(Team.name == data.away_team).first()

    if not home_team or not away_team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Une ou les deux équipes sont introuvables dans la base de données.",
        )

    # 2. Appel au service ML
    ml_url = f"{settings.ML_API_URL}/predict"
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                ml_url,
                json={
                    "home_team": data.home_team,
                    "away_team": data.away_team,
                    "season": data.season,
                },
            )
        response.raise_for_status()
        ml_result = response.json()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"Erreur retournée par le service ML : {exc.response.text}",
        )
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service ML inaccessible ({settings.ML_API_URL}) : {exc}",
        )

    # 3. Extraction des résultats ML
    predicted_result = ml_result.get("predicted_result") or ml_result.get("prediction")
    confidence_score = ml_result.get("confidence") or ml_result.get("confidence_score")

    # 4. Sauvegarde dans l'historique (modèle hybride : IDs + logos)
    history_entry = PredictionHistory(
        user_id=current_user.id,
        home_team_id=home_team.id,
        away_team_id=away_team.id,
        home_team_name=home_team.name,
        home_team_logo_url=home_team.logo_url,
        away_team_name=away_team.name,
        away_team_logo_url=away_team.logo_url,
        predicted_result=str(predicted_result) if predicted_result is not None else None,
        confidence_score=float(confidence_score) if confidence_score is not None else None,
    )
    db.add(history_entry)
    db.commit()
    db.refresh(history_entry)

    # 5. Retour enrichi avec logos
    return {
        **ml_result,
        "home_team_logo_url": home_team.logo_url,
        "away_team_logo_url": away_team.logo_url,
    }


# ─────────────────────────────────────────────
# GET /predictions/history
# Historique des prédictions de l'utilisateur courant
# ─────────────────────────────────────────────
@router.get("/history", response_model=List[PredictionHistoryOut])
def get_prediction_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 50,
):
    return (
        db.query(PredictionHistory)
        .filter(PredictionHistory.user_id == current_user.id)
        .order_by(PredictionHistory.created_at.desc())
        .limit(limit)
        .all()
    )


# ─────────────────────────────────────────────
# POST /predictions/history  (save manuel — optionnel)
# ─────────────────────────────────────────────
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
    db: Session = Depends(get_db),
):
    # Résolution optionnelle des IDs à partir des noms
    home_team = db.query(Team).filter(Team.name == data.home_team_name).first()
    away_team = db.query(Team).filter(Team.name == data.away_team_name).first()

    new_prediction = PredictionHistory(
        user_id=current_user.id,
        home_team_id=home_team.id if home_team else None,
        away_team_id=away_team.id if away_team else None,
        home_team_name=data.home_team_name,
        home_team_logo_url=data.home_team_logo_url or (home_team.logo_url if home_team else None),
        away_team_name=data.away_team_name,
        away_team_logo_url=data.away_team_logo_url or (away_team.logo_url if away_team else None),
        predicted_result=data.predicted_result,
        confidence_score=data.confidence_score,
    )
    db.add(new_prediction)
    db.commit()
    db.refresh(new_prediction)
    return new_prediction


def register_routes(app):
    app.include_router(router)
