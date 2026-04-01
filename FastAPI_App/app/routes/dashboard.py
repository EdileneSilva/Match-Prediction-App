from fastapi import APIRouter, HTTPException, Path, Depends
import httpx
import logging
from sqlalchemy.orm import Session
from ..core.config import settings
from ..database import get_db
from ..models.team import Team

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/dashboard", tags=["Dashboard Proxy"])

@router.get("/upcoming")
async def proxy_upcoming(db: Session = Depends(get_db)):
    """
    Proxy vers l'API ML pour récupérer les prochains matchs.
    Synchronise également les logos localement.
    """
    target_url = f"{settings.ML_API_URL}/dashboard/upcoming"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(target_url, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            matches = data.get("matches", [])
            for m in matches:
                for side in ["home_team", "away_team"]:
                    team_data = m.get(side, {})
                    team_name = team_data.get("name")
                    logo_url = team_data.get("logo")
                    if team_name:
                        team = db.query(Team).filter(Team.name == team_name).first()
                        if team:
                            if logo_url and team.logo_url != logo_url:
                                team.logo_url = logo_url
                        else:
                            team = Team(name=team_name, logo_url=logo_url)
                            db.add(team)
            db.commit()
            return data
        except httpx.HTTPStatusError as e:
            logger.error(f"Erreur HTTP lors du proxy vers le service ML : {e.response.status_code}")
            raise HTTPException(status_code=e.response.status_code, detail="Erreur du service ML")
        except Exception as e:
            logger.error(f"Erreur lors du proxy vers le service ML : {e}")
            raise HTTPException(status_code=500, detail="Service ML indisponible")

@router.get("/standings")
async def proxy_standings(db: Session = Depends(get_db)):
    """
    Proxy vers l'API ML pour récupérer le classement.
    Synchronise également les logos localement.
    """
    target_url = f"{settings.ML_API_URL}/dashboard/standings"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(target_url, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "success":
                for s in data.get("data", []):
                    team_name = s.get("team")
                    logo_url = s.get("logo")
                    if team_name:
                        team = db.query(Team).filter(Team.name == team_name).first()
                        if team:
                            if logo_url and team.logo_url != logo_url:
                                team.logo_url = logo_url
                        else:
                            team = Team(name=team_name, logo_url=logo_url)
                            db.add(team)
                db.commit()
            return data
        except httpx.HTTPStatusError as e:
            logger.error(f"Erreur HTTP lors du proxy vers le service ML : {e.response.status_code}")
            raise HTTPException(status_code=e.response.status_code, detail="Erreur du service ML")
        except Exception as e:
            logger.error(f"Erreur lors du proxy vers le service ML : {e}")
            raise HTTPException(status_code=500, detail="Service ML indisponible")
