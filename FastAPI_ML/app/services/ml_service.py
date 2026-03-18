import random
from typing import Dict

class MLService:
    def __init__(self):
        # Ici on chargerait le modèle avec joblib.load('model.joblib')
        self.model = None
        self.is_model_loaded = False

    def predict_match(self, home_team_id: int, away_team_id: int) -> Dict:
        """
        Simule une prédiction de match.
        À l'avenir, cette méthode :
        1. Préparera les features (moyenne des buts, forme récente, etc.)
        2. Appelera self.model.predict()
        """
        results = ["HOME_WIN", "AWAY_WIN", "DRAW"]
        predicted_result = random.choice(results)
        confidence_score = round(random.uniform(0.5, 0.95), 2)
        
        return {
            "predicted_result": predicted_result,
            "confidence_score": confidence_score
        }

ml_service = MLService()
