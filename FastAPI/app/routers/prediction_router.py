from fastapi import APIRouter

router = APIRouter()

@router.post("/predict")
def predict_match():
    return {"message": "Prediction endpoint not implemented yet."}
