from typing import Any, Dict


def predict_match(_: Dict[str, Any]) -> Dict[str, Any]:
    """
    Service de prédiction minimal (stub).
    À remplacer par un vrai modèle scikit-learn.
    """
    return {"predicted_result": "DRAW", "confidence_score": 0.5}

