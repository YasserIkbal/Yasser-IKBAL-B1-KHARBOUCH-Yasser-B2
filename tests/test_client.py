"""Tests du client HTTP sans démarrer Streamlit ni l'API."""
from unittest.mock import Mock, patch

import pytest
import requests

from ui.client import APIClientError, analyser_avis


def reponse(code: int, corps: dict) -> Mock:
    resultat = Mock(status_code=code)
    resultat.json.return_value = corps
    return resultat


def test_client_envoie_un_avis_et_retourne_le_verdict():
    with patch("ui.client.requests.post", return_value=reponse(200, {"label": "POSITIVE", "score": 0.91})) as post:
        assert analyser_avis("Très bon produit") == {"label": "POSITIVE", "score": 0.91}
    post.assert_called_once()
    assert post.call_args.kwargs["json"] == {"text": "Très bon produit"}


@pytest.mark.parametrize("code", [422, 503, 500])
def test_client_traduit_les_erreurs_http(code):
    with patch("ui.client.requests.post", return_value=reponse(code, {})):
        with pytest.raises(APIClientError):
            analyser_avis("texte")


def test_client_traduit_api_injoignable():
    with patch("ui.client.requests.post", side_effect=requests.ConnectionError):
        with pytest.raises(APIClientError, match="injoignable"):
            analyser_avis("texte")


def test_client_refuse_une_reponse_invalide():
    with patch("ui.client.requests.post", return_value=reponse(200, {"label": "BOF", "score": 2})):
        with pytest.raises(APIClientError, match="Réponse invalide"):
            analyser_avis("texte")
