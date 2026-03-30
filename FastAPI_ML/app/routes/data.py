from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.preparation import preparation_service

router = APIRouter(tags=["Data"])

@router.post("/data/prepare")
def prepare_data(db: Session = Depends(get_db)):

    result = preparation_service.run(db)
    return result