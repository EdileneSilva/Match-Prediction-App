from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, FastAPI
from ..services.preparation import preparation_service
from sqlalchemy.orm import Session
from ..database import get_db
from enum import Enum
import pandas as pd
import io

router = APIRouter(tags=["Ingestion"])

class Source(Enum):
    LIGUE_1 = "LIGUE_1" # https://ma-api.ligue1.fr/championships-daily-calendars/matches?timezone=Europe/Paris&daysLimit=10&lookAfter=true
    FOOTBALL_DATA = "FOOTBALL_DATA" # https://www.football-data.co.uk/francem.php
    API = "API" # https://www.api-football.com/

@router.post("/ingest")
def ingest(
    db: Session = Depends(get_db),
    source_type: Source = Source.FOOTBALL_DATA,
    file: UploadFile = File(...)
):
    """
        Ingestion d'une nouvelle source de données dans la base de données ML pour des entrainements futurs.
        Ne prend en charge que la source Source.FOOTBALL_DATA (pour le moment).

        :param db: Session: Injection de la base de données
        :param source_type: Source: Le type de la source initiale qui déterminera quel service appeler
        :param file: Source: Le fichier .csv (Source.FOOTBALL_DATA) importé

        Returns:
            dict: Un message de confirmation ou l'état de l'ingestion.
    """
    try:
        # Récupération du fichier
        contents = file.file.read()
        df = pd.read_csv(io.BytesIO(contents))

        if source_type == Source.FOOTBALL_DATA:
            # Préparation des données
            return preparation_service.run(db, df)
        else:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(f'Type de source ${source_type} non pris en charge')
            )
        # Gérer les autres source_type ici

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

def register_routes(app: FastAPI):
    app.include_router(router)