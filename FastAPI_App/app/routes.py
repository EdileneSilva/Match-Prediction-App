from fastapi import APIRouter, FastAPI


router = APIRouter()


@router.get("/", tags=["Root"])
def root():
    return {"message": "Match Prediction App - Application API"}


def register_routes(app: FastAPI) -> None:
    """
    Point central pour enregistrer toutes les routes de l'API Application.
    À enrichir avec les sous-routeurs (auth, users, predictions...).
    """
    app.include_router(router)

