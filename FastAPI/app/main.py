from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth_router, prediction_router, user_router

app = FastAPI(
    title="Match Prediction App",
    description="API de prédiction de résultats Ligue 1",
    version="0.1.0"
)

# CORS pour Vue.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
app.include_router(user_router.router, prefix="/users", tags=["Users"])
app.include_router(prediction_router.router, prefix="/predictions", tags=["Predictions"])

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "app-service"}
