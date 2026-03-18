from fastapi import APIRouter, FastAPI


router = APIRouter()


@router.get("/", tags=["Root"])
def root():
    return {"message": "Match Prediction App - Application API"}


from .auth import router as auth_router
from .prediction import router as prediction_router

def register_routes(app: FastAPI) -> None:
    """
    Point central pour enregistrer toutes les routes de l'API Application.
    À enrichir avec les sous-routeurs (auth, users, predictions...).
    """
    app.include_router(router)
    app.include_router(auth_router)
    app.include_router(prediction_router)

