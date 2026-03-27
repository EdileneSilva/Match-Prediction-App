from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.team import Team as TeamModel
from ..schemas.team import Team as TeamSchema

router = APIRouter(prefix="/teams", tags=["teams"])

@router.get("/", response_model=List[TeamSchema])
def get_teams(db: Session = Depends(get_db)):
    """Récupère la liste de toutes les équipes (Ligue 1)."""
    return db.query(TeamModel).all()
