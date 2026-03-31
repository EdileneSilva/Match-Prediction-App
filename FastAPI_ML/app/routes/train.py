from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.pipeline import pipeline_service

router = APIRouter(tags=["ML Training"])


@router.post("/train")
def train_model(db: Session = Depends(get_db)):
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
    return pipeline_service.get_history(db, limit=limit)


def register_routes(app):
    app.include_router(router)