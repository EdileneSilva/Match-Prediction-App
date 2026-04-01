from fastapi import APIRouter, FastAPI


router = APIRouter()


@router.get("/", tags=["Root"])
def root():
    return {"message": "Match Prediction App - Application API"}


from .auth import router as auth_router
from .prediction import router as prediction_router
from .dashboard import router as dashboard_router

def register_routes(app: FastAPI) -> None:
    """
    Point central pour enregistrer toutes les routes de l'API Application.
    Désormais concentré sur l'authentification et les services utilisateur.
    """
    app.include_router(router)
    app.include_router(auth_router)
    app.include_router(prediction_router)
    app.include_router(dashboard_router)

