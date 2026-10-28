"""Client HTTP minimal de l'API de sentiment."""
from __future__ import annotations

import os
from typing import Any

import requests

API_URL = os.getenv("API_URL", "http://localhost:8000")
LABELS = {"POSITIVE", "NEGATIVE", "INDETERMINE"}


class APIClientError(Exception):
    """Erreur traduisible pour l'utilisateur de l'interface."""


def analyser_avis(
    texte: str, base_url: str = API_URL, timeout: float = 5.0
) -> dict[str, Any]:
    """Envoie un avis à l'API et renvoie sa réponse JSON."""
    try:
        response = requests.post(
            f"{base_url.rstrip('/')}/predict",
            json={"text": texte},
            timeout=timeout,
        )
    except requests.RequestException as erreur:
        raise APIClientError(
            "API injoignable : démarrez l'API avec `uvicorn api.main:app`."
        ) from erreur
    if response.status_code == 422:
        raise APIClientError("Avis invalide : saisissez un texte non vide de 1 à 2000 caractères.")
    if response.status_code == 503:
        raise APIClientError("Service momentanément indisponible : modèle non chargé.")
    if response.status_code >= 400:
        raise APIClientError("L'API a rencontré une erreur interne. Réessayez plus tard.")
    try:
        resultat = response.json()
    except ValueError as erreur:
        raise APIClientError("Réponse invalide reçue de l'API.") from erreur
    try:
        valide = (
            isinstance(resultat, dict)
            and resultat.get("label") in LABELS
            and 0 <= float(resultat.get("score", -1)) <= 1
        )
    except (TypeError, ValueError):
        valide = False
    if not valide:
        raise APIClientError("Réponse invalide reçue de l'API.")
    return resultat


predict = analyser_avis
