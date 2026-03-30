from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.pipeline import pipeline_service

router = APIRouter(tags=["ML Training"])


@router.post("/train")
def train_model(db: Session = Depends(get_db)):
    """
    Lance le pipeline complet d'entraînement :
    1. Lit les données depuis match_stats
    2. Entraîne le modèle
    3. Sauvegarde le joblib
    4. Peuple team_stats_reference
    5. Enregistre les métriques dans train_log
    """
    try:
        result = pipeline_service.train(db)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        import traceback
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=traceback.format_exc()
        )


@router.get("/train/history")
def get_train_history(limit: int = 20, db: Session = Depends(get_db)):
    """Retourne l'historique des entraînements avec leurs métriques."""
    return pipeline_service.get_history(db, limit=limit)


def register_routes(app):
    app.include_router(router)