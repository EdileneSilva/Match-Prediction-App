import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.pipeline import pipeline_service
from ..core.auth import require_api_key

logger = logging.getLogger(__name__)

router = APIRouter(tags=["ML Training"])


@router.post("/train")
def train_model(
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key),
):
    try:
        return pipeline_service.train(db)
    except Exception as e:
        logger.exception("Training failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Model training failed. Check server logs for details.",
        )


@router.get("/train/history")
def get_train_history(
    limit: int = 20,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key),
):
    return pipeline_service.get_history(db, limit=limit)


def register_routes(app):
    app.include_router(router)