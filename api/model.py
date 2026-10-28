from typing import Literal, TypedDict

from api.schemas import Label
from src.predict import ModelLabel, Prediction, predict

SEUIL_ABSTENTION = 0.60
ETIQUETTES_CONTRAT: dict[ModelLabel, Label] = {
    "positive": "POSITIVE",
    "negative": "NEGATIVE",
}


class SentimentPrediction(TypedDict):
    label: Literal["POSITIVE", "NEGATIVE", "INDETERMINE"]
    score: float


def verifier_classes(modele: object) -> None:
    classes = getattr(modele, "classes", None)
    if classes is None:
        classes = getattr(modele, "classes_", None)
    if classes is None:
        raise ValueError("le modèle ne fournit pas de classes")
    inconnues = {str(classe).lower() for classe in classes} - set(ETIQUETTES_CONTRAT)
    if inconnues or {str(classe).lower() for classe in classes} != set(ETIQUETTES_CONTRAT):
        raise ValueError(f"classes de modèle inattendues : {sorted(map(str, classes))}")

class SentimentClassifier:
    def __init__(self, modele: object | None = None) -> None:
        if modele is not None:
            verifier_classes(modele)

    def predict(self, text: str) -> SentimentPrediction:
        resultat: Prediction = predict(text)
        score = resultat["score"]
        label = "INDETERMINE" if score < SEUIL_ABSTENTION else ETIQUETTES_CONTRAT[resultat["label"]]
        return {"label": label, "score": score}
