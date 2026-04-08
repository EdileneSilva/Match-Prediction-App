from fastapi import APIRouter, HTTPException, Path
import httpx
import logging
from ..core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/dashboard", tags=["Dashboard Proxy"])

@router.get("/upcoming")
async def proxy_upcoming():
    """
    Proxy vers l'API ML pour récupérer les prochains matchs.
    """
    target_url = f"{settings.ML_API_URL}/dashboard/upcoming"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(target_url, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Erreur HTTP lors du proxy vers le service ML : {e.response.status_code}")
            raise HTTPException(status_code=e.response.status_code, detail="Erreur du service ML")
        except Exception as e:
            logger.error(f"Erreur lors du proxy vers le service ML : {e}")
            raise HTTPException(status_code=500, detail="Service ML indisponible")

@router.get("/standings")
async def proxy_standings():
    """
    Proxy vers l'API ML pour récupérer le classement.
    """
    target_url = f"{settings.ML_API_URL}/dashboard/standings"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(target_url, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Erreur HTTP lors du proxy vers le service ML : {e.response.status_code}")
            raise HTTPException(status_code=e.response.status_code, detail="Erreur du service ML")
        except Exception as e:
            logger.error(f"Erreur lors du proxy vers le service ML : {e}")
            raise HTTPException(status_code=500, detail="Service ML indisponible")


@router.get("/goals-stats")
async def proxy_goals_stats():
    """
    Proxy vers l'API ML pour récupérer les stats buts réelles.
    """
    target_url = f"{settings.ML_API_URL}/dashboard/goals-stats"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(target_url, timeout=15.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Erreur HTTP lors du proxy vers le service ML : {e.response.status_code}")
            raise HTTPException(status_code=e.response.status_code, detail="Erreur du service ML")
        except Exception as e:
            logger.error(f"Erreur lors du proxy vers le service ML : {e}")
            raise HTTPException(status_code=500, detail="Service ML indisponible")
