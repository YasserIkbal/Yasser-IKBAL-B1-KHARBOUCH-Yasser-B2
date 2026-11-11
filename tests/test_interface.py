"""Tests du contrat de présentation de l'interface."""
from ui.client import APIClientError


def test_verdicts_du_contrat():
    assert {"POSITIVE", "NEGATIVE", "INDETERMINE"} == {
        "POSITIVE", "NEGATIVE", "INDETERMINE"
    }


def test_message_abstention_est_actionnable():
    message = "Je ne sais pas : à faire vérifier par un humain"
    assert "vérifier" in message and "humain" in message


def test_erreur_client_est_exposable():
    assert str(APIClientError("API injoignable")) == "API injoignable"
