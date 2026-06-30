import logging
import io
from typing import Optional

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, FastAPI
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.preparation import preparation_service
from ..core.auth import require_api_key

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Ingestion"])

_MAX_UPLOAD_BYTES = 10 * 1024 * 1024  # 10 MB


@router.post("/ingest")
def ingest(
    db: Session = Depends(get_db),
    file: Optional[UploadFile] = File(None),
    _: str = Depends(require_api_key),
):
    try:
        if file is None:
            return preparation_service.run_base(db)

        if file.content_type not in ("text/csv", "application/csv", "application/octet-stream"):
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Only CSV files are accepted.",
            )

        contents = file.file.read(_MAX_UPLOAD_BYTES + 1)
        if len(contents) > _MAX_UPLOAD_BYTES:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File exceeds the 10 MB limit.",
            )

        try:
            df = pd.read_csv(io.BytesIO(contents))
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Uploaded file could not be parsed as CSV.",
            )

        return preparation_service.run(db, df)

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except Exception:
        logger.exception("Ingestion failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Data ingestion failed. Check server logs for details.",
        )


def register_routes(app: FastAPI):
    app.include_router(router)