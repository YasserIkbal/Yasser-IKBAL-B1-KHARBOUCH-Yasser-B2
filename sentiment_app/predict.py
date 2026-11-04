"""Prédiction de sentiment, utilisable depuis le dépôt ou une roue installée."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Literal, TypedDict, cast

import joblib

ModelLabel = Literal["positive", "negative"]
MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"


class Prediction(TypedDict):
    label: ModelLabel
    score: float


def chemin_modele() -> Path:
    """Renvoie le modèle configuré, ou le chemin local du dépôt en développement."""
    valeur = os.environ.get("SENTIMENT_MODELE")
    return Path(valeur).expanduser() if valeur else MODELE


@lru_cache(maxsize=1)
def charger_modele():
    """Charge le modèle une seule fois par processus."""
    chemin = chemin_modele()
    if not chemin.exists():
        raise FileNotFoundError(
            f"modèle absent : {chemin}. Définissez SENTIMENT_MODELE ou entraînez le modèle."
        )
    return joblib.load(chemin)


def predict(texte: str) -> Prediction:
    """Renvoie une étiquette et la confiance associée."""
    if not isinstance(texte, str) or not texte.strip():
        raise ValueError("texte vide")
    pipeline = charger_modele()
    etiquette = cast(ModelLabel, str(pipeline.predict([texte])[0]).lower())
    if etiquette not in {"positive", "negative"}:
        raise ValueError(f"étiquette de modèle inconnue : {etiquette}")
    score = float(pipeline.predict_proba([texte]).max())
    return {"label": etiquette, "score": round(score, 4)}

